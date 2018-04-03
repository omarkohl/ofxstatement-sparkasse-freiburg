import copy
import os
from decimal import Decimal
from datetime import datetime

import pytest


DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
    )


CSV_LINE = {
    'Auftragskonto':                     '12345678',
    'Buchungstag':                       '28.03.18',
    'Valutadatum':                       '03.04.18',
    'Buchungstext':                      'FOLGELASTSCHRIFT',
    'Verwendungszweck':                  '1234123412341 1234123412 MIETE04/18 ',
    'Glaeubiger ID':                     'DE12ZZZ00000123412',
    'Mandatsreferenz':                   '1234-1234123412341-12',
    'Kundenreferenz (End-to-End)':       '',
    'Sammlerreferenz':                   '',
    'Lastschrift Ursprungsbetrag':       '',
    'Auslagenersatz Ruecklastschrift':   '',
    'Beguenstigter/Zahlungspflichtiger': 'ASDF Immobilien GmbH',
    'Kontonummer/IBAN':                  'DE12341234123412341234',
    'BIC (SWIFT-Code)':                  'ABCDABCDABC',
    'Betrag':                            '-1234,56',
    'Waehrung':                          'EUR',
    'Info':                              'Umsatz vorgemerkt',
    }


def test_parser_can_be_created():
    from ofxstatement.plugins.germany_sparkasse_freiburg import SparkasseFreiburgParser
    parser = SparkasseFreiburgParser('random_file_name', 'utf-8', '11111111')
    assert parser is not None


def test_parse_single_record():
    from ofxstatement.plugins.germany_sparkasse_freiburg import SparkasseFreiburgParser
    parser = SparkasseFreiburgParser('random_file_name', 'utf-8', '11111111')
    line = copy.deepcopy(CSV_LINE)
    statement_line = parser.parse_record(line)
    assert statement_line.amount == Decimal('-1234.56')
    assert statement_line.trntype == 'DEBIT'
    assert statement_line.date == datetime(2018, 4, 3, 0, 0)
    assert statement_line.payee == '1234123412341 1234123412 MIETE04/18; ASDF Immobilien GmbH'
    assert statement_line.memo == 'FOLGELASTSCHRIFT; IBAN: DE12341234123412341234; BIC: ABCDABCDABC'
    assert statement_line.id == '8484592452219632'


def test_simple1_csv():
    """
    Test that the file simple1.csv is parsed correctly
    """
    from ofxstatement.plugins.germany_sparkasse_freiburg import SparkasseFreiburgParser
    # Get data from file
    parser = SparkasseFreiburgParser(
        os.path.join(DATA_DIR, 'simple1.csv'),
        'cp1252',
        '11111111',
        )
    statement = parser.parse()
    for l in statement.lines:
        print(l)
    expected_amounts = [Decimal('-1234.56'), Decimal('123')]
    assert expected_amounts == [l.amount for l in statement.lines]
    expected_ids = ['8484592452219632', '2023350027454340']
    assert expected_ids == [l.id for l in statement.lines]

    assert statement.currency == 'EUR'
    assert statement.bank_id == 'FRSPDE66XXX'
    assert statement.account_id == '11111111'

    # gnuCash doesn't seem to use or require the 'balance' so we don't
    # calculate it
    assert statement.start_date == None
    assert statement.start_balance == None
    assert statement.end_date == None
    assert statement.end_balance == None


def test_long_payee():
    from ofxstatement.plugins.germany_sparkasse_freiburg import SparkasseFreiburgParser
    line = copy.deepcopy(CSV_LINE)
    line['Beguenstigter/Zahlungspflichtiger'] = '1u1 Telecom GmbH        ' + \
        '                                              Elgendorfer Str. 57 '
    line['Verwendungszweck'] = 'KD-Nr. A123412341 / RG-Nr. 123412341234 ' + \
        '/ Beleg-Nr. 1234123412341234123412341234'
    parser = SparkasseFreiburgParser('random_file_name', 'utf-8', '11111111')
    statement_line = parser.parse_record(line)
    assert statement_line.payee == 'KD-Nr. A123412341 / RG-Nr. 123412341234' + \
        ' / Bele...; 1u1 Telecom GmbH Elgendorfer Str. 57'


def test_no_recipient():
    from ofxstatement.plugins.germany_sparkasse_freiburg import SparkasseFreiburgParser
    line = copy.deepcopy(CSV_LINE)
    line['Beguenstigter/Zahlungspflichtiger'] = ''
    line['Verwendungszweck'] = 'KD-Nr. A123412341 / RG-Nr. 123412341234'
    parser = SparkasseFreiburgParser('random_file_name', 'utf-8', '11111111')
    statement_line = parser.parse_record(line)
    assert statement_line.payee == 'KD-Nr. A123412341 / RG-Nr. 123412341234' + \
        '; UNBEKANNT'

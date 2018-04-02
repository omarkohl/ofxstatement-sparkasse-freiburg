import glob
import os
import re
from subprocess import check_call
from shutil import copyfile

from bs4 import BeautifulSoup
import pytest


DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
    )


# The purpose of this constant is to easily overwrite the test files when some
# change in the expected files is required (e.g. the test data was modified or
# the output format legitimately needs to change). For normal tests this should
# not be modified!
OVERWRITE_EXPECTED_FILES=False


@pytest.mark.parametrize(
    'src_csv',
    glob.glob(os.path.join(DATA_DIR, '*.csv')),
    )
def test_end2end_conversion(src_csv, ofxstatement_bin_path, tmpdir, replace_config):
    """
    Test correct conversion of all CSV files in the 'data' directory. This in
    an end to end test that uses the installed 'ofxstatement' binary to
    generate an OFX file (use the --ofxstatement-bin cmd parameter to use a
    different binary). The OFX file is then compared with a correct version
    available in the 'data' directory. Since OFX is just XML we also compare a
    prettified version of both files because then it is easier to spot
    differences should they occur.
    """
    temp_ofx = str(tmpdir / 'temp.ofx')
    temp_pretty_xml = str(tmpdir / 'temp-pretty.xml')
    expected_ofx = src_csv[:-4] + '.ofx'
    expected_pretty_xml = src_csv[:-4] + '-pretty.xml'

    cmd = [
        ofxstatement_bin_path,
        'convert',
        '-t',
        'sparkasse_freiburg',
        src_csv,
        temp_ofx,
        ]
    check_call(cmd)

    with open(temp_ofx, mode='rt', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')
    with open(temp_pretty_xml, mode='wt', encoding='utf-8') as f:
        f.write(soup.prettify())
    if OVERWRITE_EXPECTED_FILES:
        copyfile(temp_ofx, expected_ofx)
        copyfile(temp_pretty_xml, expected_pretty_xml)
    # Compary pretty versions so the possible differences are easier to see
    with open(expected_pretty_xml, mode='rt', encoding='utf-8') as f:
        expected_content = f.read()
    with open(temp_pretty_xml, mode='rt', encoding='utf-8') as f:
        available_content = f.read()
    # DTSERVER is the time the document was generated so it will never match
    # therefore we remove it
    expected_content = re.sub(
        '<DTSERVER>.*</DTSERVER>',
        '',
        expected_content,
        flags=re.DOTALL,
        )
    available_content = re.sub(
        '<DTSERVER>.*</DTSERVER>',
        '',
        available_content,
        flags=re.DOTALL,
        )
    assert expected_content == available_content
    # To ensure no differences were hidden by XML-parsing we compare the
    # original OFX files
    with open(expected_ofx, mode='rt', encoding='utf-8') as f:
        expected_content = f.read()
    with open(temp_ofx, mode='rt', encoding='utf-8') as f:
        available_content = f.read()
    # DTSERVER is the time the document was generated so it will never match
    # therefore we remove it
    expected_content = re.sub(
        '<DTSERVER>.*</DTSERVER>',
        '',
        expected_content,
        )
    available_content = re.sub(
        '<DTSERVER>.*</DTSERVER>',
        '',
        available_content,
        )
    assert expected_content == available_content

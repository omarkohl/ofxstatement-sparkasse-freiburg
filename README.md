# ofxstatement plugin for Sparkasse Freiburg-Nördlicher Breisgau

[![Build Status](https://travis-ci.org/omarkohl/ofxstatement-sparkasse-freiburg.svg?branch=master)](https://travis-ci.org/omarkohl/ofxstatement-sparkasse-freiburg)
[![PyPI](https://img.shields.io/pypi/v/ofxstatement-sparkasse-freiburg.svg)](https://pypi.python.org/pypi/ofxstatement-sparkasse-freiburg)

This is an ofxstatement plugin for the German bank Sparkasse
Freiburg-Nördlicher Breisgau (short: Sparkasse Freiburg).

This plugin has no affiliation with or endorsement by [Sparkasse
Freiburg-Nördlicher Breisgau](https://www.sparkasse-freiburg.de/). The only
reason for using the name is to aid people looking for a tool to convert that
bank's CSV transaction exports to OFX.

[ofxstatement](https://github.com/kedder/ofxstatement) is a tool to convert
proprietary bank statement to OFX format, suitable for importing to GnuCash.
Plugin for ofxstatement parses a particular proprietary bank statement format
and produces common data structure, that is then formatted into an OFX file.

Users of ofxstatement have developed several plugins for their banks. They are
listed on the main [ofxstatement](https://github.com/kedder/ofxstatement) site.
If your bank is missing, you can develop your own plugin.


## Usage

To use this plugin install it. For example:

```bash
pip3 install --user ofxstatement-sparkasse-freiburg
```

Edit the configuration:

```bash
ofxstatement edit-config
```

Add something like this:

```
[sparkasse_freiburg]
plugin = germany_sparkasse_freiburg
account = 123456789
```

*account* is you bank account number (Kontonummer).

Other possible settings are:

* **encoding:** The encoding of the CSV file (default is Windows 1252 ANSI:
  cp1252)

Then download the CSV files (CSV-CAMT format) from you online banking account
and convert it as follows:

```bash
ofxstatement convert -t sparkasse_freiburg EXAMPLE.csv EXAMPLE.ofx
```

The resulting .ofx file can then be imported in gnuCash or similar software.

**Note:** Beware that some things (such as balance calculation) were left out
because they are not needed by gnuCash. Open a ticket or send a pull request if
something is missing for your use case.


# Development

It is recommended to use *virtualenv* to make a clean development environment.

```bash
git clone https://github.com/omarkohl/ofxstatement-sparkasse-freiburg
cd ofxstatement-sparkasse-freiburg
make venv
source .venv/bin/activate
```

This will download all the dependencies and install them into your virtual
environment. After this, you should be able to do::

```bash
ofxstatement list-plugins
```

Expected output:

```
The following plugins are available:

  germany_sparkasse_freiburg Plugin for German bank Sparkasse Freiburg
```

## Tests

Execute:

```bash
make test
```

### Integration tests

Part of the tests are integration (or end to end) tests that test the complete
conversion from CSV to OFX files. You can find these files under *tests/data* .
Every *.csv* file is verified to be converted to the corresponding *.ofx* file.
Additionally the *-pretty.xml* files contain a pretty version of the resulting
OFX (which actually is just XML).

To add a new .csv example simply include it in said directory and edit
*tests/test_integration.py* . Set `OVERWRITE_EXPECTED_FILES` to `True` and then
execute the tests. Commit the content of *tests/data* .


## Improvements

In general the plugin tries to be simple and not convert any values that are
currently not needed. If something is missing feel free to open an issue or
even better send a pull requests.

Some things which may be worth modifying:

* The bank_id is currently hardcoded to Sparkasse Freiburg's BIC
* The currency of the account is also hardcoded to EUR
* The StatementLine.id (becomes OFX's FITID) is calculated by hashing date,
  payee, memo and amount and then truncated. FITID should always be unique for
  the entire account history to detect transaction duplicates.
* OFX's NAME field (.payee in the code) is made out of the sender/receiver +
  the subject (Verwendungszweck). This could be made configurable.
* OFX's MEMO field (.memo in the code) is made out of Buchungstext, Kontonummer
  and BIC.
* trntype is currently only ever set to DEBIT or CREDIT. Using 'Buchungstext'
  it could be improved.

# ofxstatement plugin for Sparkasse Freiburg-Nördlicher Breisgau

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


## Setting up development environment

It is recommended to use *virtualenv* make a clean development environment.

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

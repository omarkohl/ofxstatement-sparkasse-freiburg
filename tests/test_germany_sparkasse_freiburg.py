def test_parser_can_be_created():
    from ofxstatement.plugins.germany_sparkasse_freiburg import SparkasseFreiburgParser
    parser = SparkasseFreiburgParser([])
    assert parser is not None

from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import StatementLine


class SparkasseFreiburgPlugin(Plugin):
    """Plugin for German bank Sparkasse Freiburg
    """

    def get_parser(self, filename):
        return SparkasseFreiburgParser(filename)


class SparkasseFreiburgParser(CsvStatementParser):

    def split_records(self):
        """Return iterable object consisting of a line per transaction
        """
        return []

    def parse_record(self, line):
        """Parse given transaction line and return StatementLine object
        """
        return StatementLine()

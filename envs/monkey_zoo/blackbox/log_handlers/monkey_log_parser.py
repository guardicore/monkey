import logging
import re

LOGGER = logging.getLogger(__name__)


class MonkeyLogParser(object):

    def __init__(self, log_path):
        self.log_path = log_path
        self.log_contents = self.read_log()

    def read_log(self):
        with open(self.log_path, 'r') as log:
            return log.read()

    def print_errors(self):
        errors = MonkeyLogParser.get_errors(self.log_contents)
        if len(errors) > 0:
            LOGGER.info("Found {} errors:".format(len(errors)))
            for index, error_line in enumerate(errors):
                LOGGER.info("Err #{}: {}".format(index, error_line))
        else:
            LOGGER.info("No errors!")

    @staticmethod
    def get_errors(log_contents):
        searcher = re.compile(r"^.*:ERROR].*$", re.MULTILINE)
        return searcher.findall(log_contents)

    def print_warnings(self):
        warnings = MonkeyLogParser.get_warnings(self.log_contents)
        if len(warnings) > 0:
            LOGGER.info("Found {} warnings:".format(len(warnings)))
            for index, warning_line in enumerate(warnings):
                LOGGER.info("Warn #{}: {}".format(index, warning_line))
        else:
            LOGGER.info("No warnings!")

    @staticmethod
    def get_warnings(log_contents):
        searcher = re.compile(r"^.*:WARNING].*$", re.MULTILINE)
        return searcher.findall(log_contents)

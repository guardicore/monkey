import re


class LogParser(object):

    def __init__(self, log_path):
        self.log_path = log_path
        self.log_contents = self.read_log()

    def read_log(self):
        with open(self.log_path, 'r') as log:
            return log.read()

    def print_errors(self):
        print("Errors:")
        for error_line in LogParser.get_errors(self.log_contents):
            print(error_line)

    @staticmethod
    def get_errors(log_contents):
        searcher = re.compile(r"^.*:ERROR].*$", re.MULTILINE)
        return searcher.findall(log_contents)

    def print_warnings(self):
        print("Warnings:")
        for warning_line in LogParser.get_warnings(self.log_contents):
            print(warning_line)

    @staticmethod
    def get_warnings(log_contents):
        searcher = re.compile(r"^.*:WARNING].*$", re.MULTILINE)
        return searcher.findall(log_contents)

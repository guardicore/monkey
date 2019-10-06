import re


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
            print("Found {} errors:".format(len(errors)))
            for error_line in errors:
                print(error_line)
        else:
            print("No errors!")

    @staticmethod
    def get_errors(log_contents):
        searcher = re.compile(r"^.*:ERROR].*$", re.MULTILINE)
        return searcher.findall(log_contents)

    def print_warnings(self):
        warnings = MonkeyLogParser.get_warnings(self.log_contents)
        if len(warnings) > 0:
            print("Found {} warnings:".format(len(warnings)))
            for warning_line in warnings:
                print(warning_line)
        else:
            print("No warnings!")

    @staticmethod
    def get_warnings(log_contents):
        searcher = re.compile(r"^.*:WARNING].*$", re.MULTILINE)
        return searcher.findall(log_contents)

LOG_INIT_MESSAGE = "Analysis didn't run."


class AnalyzerLog(object):

    def __init__(self, analyzer_name):
        self.contents = LOG_INIT_MESSAGE
        self.name = analyzer_name

    def clear(self):
        self.contents = ""

    def add_entry(self, message):
        self.contents = "{}\n{}".format(self.contents, message)

    def get_contents(self):
        return "{}: {}\n".format(self.name, self.contents)

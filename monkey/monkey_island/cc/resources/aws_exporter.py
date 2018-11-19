from exporter import Exporter

class AWSExporter(Exporter):

    def __init__(self):
        Exporter.__init__(self)

    def handle_report(self, report_json):
        pass
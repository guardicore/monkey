class Exporter(object):
    def __init__(self):
        pass

    @staticmethod
    def handle_report(report_json: dict) -> str:
        """
        Get the report, export it, and report back a user-facing message on success.
        """
        raise NotImplementedError

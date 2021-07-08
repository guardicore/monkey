from monkey_island.cc.services.reporting.report import ReportService


class RansomwareReportService:
    def __init__(self):
        pass

    @staticmethod
    def get_exploitation_stats():
        scanned = ReportService.get_scanned()
        exploited = ReportService.get_exploited()

        return {"scanned": scanned, "exploited": exploited}

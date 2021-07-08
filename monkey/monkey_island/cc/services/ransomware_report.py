from monkey_island.cc.services.reporting.report import ReportService


class RansomwareReportService:
    @staticmethod
    def get_exploitation_details():
        scanned = ReportService.get_scanned()
        exploited = ReportService.get_exploited()

        return {"scanned": scanned, "exploited": exploited}

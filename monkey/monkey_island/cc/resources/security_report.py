from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.services.reporting.report import ReportService


class SecurityReport(AbstractResource):
    urls = ["/api/report/security"]

    def get(self):
        ReportService.update_report()
        return ReportService.get_report()

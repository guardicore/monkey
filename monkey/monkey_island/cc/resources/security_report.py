from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.reporting.report import ReportService


class SecurityReport(AbstractResource):
    urls = ["/api/report/security"]

    @jwt_required
    def get(self):
        return ReportService.get_report()

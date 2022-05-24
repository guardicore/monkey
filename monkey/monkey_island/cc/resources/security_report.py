from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.reporting.report import ReportService


class SecurityReport(AbstractResource):
    # API Spec: This is an action and there's no "resource"; RPC-style endpoint?
    urls = ["/api/report/security"]

    @jwt_required
    def get(self):
        return ReportService.get_report()

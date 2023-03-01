from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.reporting.report import ReportService


class SecurityReport(AbstractResource):
    urls = ["/api/report/security"]

    @jwt_required
    def get(self):
        ReportService.update_report()
        return ReportService.get_report()

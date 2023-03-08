from flask_security import auth_token_required, roles_required

from common import AccountRoles
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.reporting.report import ReportService


class SecurityReport(AbstractResource):
    urls = ["/api/report/security"]

    @auth_token_required
    @roles_required(AccountRoles.ISLAND_INTERFACE.name)
    def get(self):
        ReportService.update_report()
        return ReportService.get_report()

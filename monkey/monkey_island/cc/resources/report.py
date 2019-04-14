import flask_restful

from monkey_island.cc.auth import jwt_required
from monkey_island.cc.services.report import ReportService

__author__ = "itay.mizeretz"


class Report(flask_restful.Resource):

    @jwt_required()
    def get(self):
        return ReportService.get_report()

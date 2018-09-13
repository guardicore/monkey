import flask_restful

from cc.auth import jwt_required
from cc.services.report import ReportService

__author__ = "itay.mizeretz"


class Report(flask_restful.Resource):

    @jwt_required()
    def get(self):
        return ReportService.get_report()

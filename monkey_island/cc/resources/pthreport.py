import flask_restful

from cc.auth import jwt_required
from cc.services.pth_report import PTHReportService

__author__ = "maor.rayzin"


class PTHReport(flask_restful.Resource):

    @jwt_required()
    def get(self):
        return PTHReportService.get_report()

import flask_restful

from cc.services.report import ReportService

__author__ = "itay.mizeretz"


class Report(flask_restful.Resource):
    def get(self):
        return ReportService.get_report()

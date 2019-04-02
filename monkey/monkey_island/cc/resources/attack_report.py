import flask_restful
from flask import jsonify
from cc.auth import jwt_required
from cc.services.attack.attack_report import AttackReportService

__author__ = "itay.mizeretz"


class AttackReport(flask_restful.Resource):

    @jwt_required()
    def get(self):
        return jsonify(AttackReportService.get_report())

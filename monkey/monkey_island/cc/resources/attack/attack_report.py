import flask_restful
from flask import jsonify
from monkey_island.cc.auth import jwt_required
from monkey_island.cc.services.attack.attack_report import AttackReportService

__author__ = "VakarisZ"


class AttackReport(flask_restful.Resource):

    @jwt_required()
    def get(self):
        return jsonify(AttackReportService.get_latest_report()['techniques'])

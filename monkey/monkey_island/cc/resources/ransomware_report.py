import flask_restful
from flask import jsonify

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.ransomware_report import get_propagation_stats


class RansomwareReport(flask_restful.Resource):
    @jwt_required
    def get(self):
        return jsonify({"report": None, "propagation_stats": get_propagation_stats()})

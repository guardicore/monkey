import flask_restful
from flask import jsonify

from monkey_island.cc.resources.auth.auth import jwt_required


class RansomwareReport(flask_restful.Resource):
    @jwt_required
    def get(self):
        return jsonify({"report": None})

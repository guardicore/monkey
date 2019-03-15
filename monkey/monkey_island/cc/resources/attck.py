import flask_restful
from flask import jsonify

from cc.auth import jwt_required
from cc.services.attck.attck import AttckService


class AttckConfiguration(flask_restful.Resource):
    @jwt_required()
    def get(self):
        return jsonify(schema=AttckService.get_config_schema(),
                       configuration=AttckService.get_config())


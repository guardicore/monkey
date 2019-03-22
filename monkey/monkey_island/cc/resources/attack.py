import flask_restful
import json
from flask import jsonify, request

from cc.auth import jwt_required
from cc.services.attack.attack import AttackService


class AttckConfiguration(flask_restful.Resource):
    @jwt_required()
    def get(self):
        return jsonify(configuration=AttackService.get_config()['properties'])

    @jwt_required()
    def post(self):
        AttackService.update_config({'properties': json.loads(request.data)})
        return {}


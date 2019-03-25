import flask_restful
import json
from flask import jsonify, request

from cc.auth import jwt_required
from cc.services.attack.attack import AttackService


class AttackConfiguration(flask_restful.Resource):
    @jwt_required()
    def get(self):
        return jsonify(configuration=AttackService.get_config()['properties'])

    @jwt_required()
    def post(self):
        config_json = json.loads(request.data)
        if 'reset_attack_matrix' in config_json:
            AttackService.reset_config()
            return jsonify(configuration=AttackService.get_config()['properties'])
        else:
            AttackService.update_config({'properties': json.loads(request.data)})
            return {}


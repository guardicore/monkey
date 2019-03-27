import flask_restful
import json
from flask import jsonify, request

from cc.auth import jwt_required
from cc.services.attack.attack_config import *


class AttackConfiguration(flask_restful.Resource):
    @jwt_required()
    def get(self):
        return jsonify(configuration=get_config()['properties'])

    @jwt_required()
    def post(self):
        """
        Based on request content this endpoint either resets ATT&CK configuration or updates it.
        :return: Technique types dict with techniques on reset and nothing on update
        """
        config_json = json.loads(request.data)
        if 'reset_attack_matrix' in config_json:
            reset_config()
            return jsonify(configuration=get_config()['properties'])
        else:
            update_config({'properties': json.loads(request.data)})
            apply_to_monkey_config()
            return {}


import flask_restful
from flask import current_app, json, jsonify, request

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.attack.attack_config import AttackConfig

__author__ = "VakarisZ"


class AttackConfiguration(flask_restful.Resource):
    @jwt_required
    def get(self):
        return current_app.response_class(json.dumps({"configuration": AttackConfig.get_config()},
                                                     indent=None,
                                                     separators=(",", ":"),
                                                     sort_keys=False) + "\n",
                                          mimetype=current_app.config['JSONIFY_MIMETYPE'])

    @jwt_required
    def post(self):
        """
        Based on request content this endpoint either resets ATT&CK configuration or updates it.
        :return: Technique types dict with techniques on reset and nothing on update
        """
        config_json = json.loads(request.data)
        if 'reset_attack_matrix' in config_json:
            AttackConfig.reset_config()
            return jsonify(configuration=AttackConfig.get_config())
        else:
            AttackConfig.update_config({'properties': json.loads(request.data)})
            AttackConfig.apply_to_monkey_config()
            return {}

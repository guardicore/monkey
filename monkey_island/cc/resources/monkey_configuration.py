import json

import flask_restful
from flask import request, jsonify

from cc.auth import jwt_required
from cc.services.config import ConfigService

__author__ = 'Barak'


class MonkeyConfiguration(flask_restful.Resource):
    @jwt_required()
    def get(self):
        return jsonify(schema=ConfigService.get_config_schema(), configuration=ConfigService.get_config(False, True))

    @jwt_required()
    def post(self):
        config_json = json.loads(request.data)
        if config_json.has_key('reset'):
            ConfigService.reset_config()
        else:
            ConfigService.update_config(config_json, should_encrypt=True)
        return self.get()

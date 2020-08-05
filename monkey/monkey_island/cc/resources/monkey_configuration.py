import json

import flask_restful
from flask import abort, jsonify, request

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.config import ConfigService

__author__ = 'Barak'


class MonkeyConfiguration(flask_restful.Resource):
    @jwt_required
    def get(self):
        return jsonify(schema=ConfigService.get_config_schema(), configuration=ConfigService.get_config(False, True))

    @jwt_required
    def post(self):
        config_json = json.loads(request.data)
        if 'reset' in config_json:
            ConfigService.reset_config()
        else:
            if not ConfigService.update_config(config_json, should_encrypt=True):
                abort(400)
        return self.get()

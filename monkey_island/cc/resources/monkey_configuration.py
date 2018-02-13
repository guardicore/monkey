import json

from flask import request, jsonify
import flask_restful

from cc.database import mongo
from cc.services.config import ConfigService

__author__ = 'Barak'


class MonkeyConfiguration(flask_restful.Resource):
    def get(self):
        return jsonify(schema=ConfigService.get_config_schema(), configuration=ConfigService.get_config())

    def post(self):
        config_json = json.loads(request.data)
        if config_json.has_key('reset'):
            ConfigService.reset_config()
        else:
            ConfigService.update_config(config_json, should_encrypt=True)
        return self.get()


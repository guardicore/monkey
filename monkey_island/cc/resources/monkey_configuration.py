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

        mongo.db.config.update({'name': 'newconfig'}, {"$set": config_json}, upsert=True)
        return jsonify(schema=ConfigService.get_config_schema(), configuration=ConfigService.get_config())


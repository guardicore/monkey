import json

from flask import request
import flask_restful

from cc.database import mongo

__author__ = 'Barak'


class NewConfig(flask_restful.Resource):
    def get(self):
        config = mongo.db.config.find_one({'name': 'newconfig'}) or {}
        if 'name' in config:
            del config['name']
        return config

    def post(self):
        config_json = json.loads(request.data)
        return mongo.db.config.update({'name': 'newconfig'}, {"$set": config_json}, upsert=True)

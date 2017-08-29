import json

from flask import request, jsonify
import flask_restful

from cc.database import mongo

__author__ = 'Barak'


SCHEMA = {
    'type': 'object',
    'title': 'Monkey',
    'properties': {
        'alive': {
            'title': 'Alive',
            'type': 'boolean'
        }
    },
    'options': {
        'collapsed': True
    }
}


class MonkeyConfiguration(flask_restful.Resource):
    def get(self):
        return jsonify(schema=SCHEMA, configuration=self._get_configuration())

    def post(self):
        config_json = json.loads(request.data)
        mongo.db.config.update({'name': 'newconfig'}, {"$set": config_json}, upsert=True)
        return jsonify(schema=SCHEMA, configuration=self._get_configuration())

    @classmethod
    def _get_configuration(cls):
        config = mongo.db.config.find_one({'name': 'newconfig'}) or {}
        for field in ('name', '_id'):
            config.pop(field, None)
        return config

from datetime import datetime

from flask import request, make_response, jsonify
import flask_restful

from cc.database import mongo

from cc.utils import init_collections, local_ip_addresses

__author__ = 'Barak'


class Root(flask_restful.Resource):
    def get(self, action=None):
        if not action:
            action = request.args.get('action')

        if not action:
            return jsonify(ip_addresses=local_ip_addresses(), mongo=str(mongo.db))

        elif action == "reset":
            mongo.db.config.drop()
            mongo.db.monkey.drop()
            mongo.db.telemetry.drop()
            mongo.db.usernames.drop()
            mongo.db.passwords.drop()
            mongo.db.node.drop()
            mongo.db.edge.drop()
            init_collections()
            return jsonify(status='OK')
        elif action == "killall":
            mongo.db.monkey.update({}, {'$set': {'config.alive': False, 'modifytime': datetime.now()}}, upsert=False,
                                   multi=True)
            return 200
        else:
            return make_response(400, {'error': 'unknown action'})

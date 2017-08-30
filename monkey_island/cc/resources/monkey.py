import json
from datetime import datetime, timedelta

import dateutil
from flask import request
import flask_restful

from cc.database import mongo

__author__ = 'Barak'


def update_dead_monkeys():
    # Update dead monkeys only if no living monkey transmitted keepalive in the last 10 minutes
    if mongo.db.monkey.find_one({'dead': {'$ne': True}, 'keepalive': {'$gte': datetime.now() - timedelta(minutes=10)}}):
        return

    mongo.db.monkey.update(
        {'keepalive': {'$lte': datetime.now() - timedelta(minutes=10)}, 'dead': {'$ne': True}},
        {'$set': {'dead': True, 'modifytime': datetime.now()}}, upsert=False, multi=True)


class Monkey(flask_restful.Resource):
    def get(self, guid=None, **kw):
        update_dead_monkeys()  # refresh monkeys status
        if not guid:
            guid = request.args.get('guid')
        timestamp = request.args.get('timestamp')

        if guid:
            monkey_json = mongo.db.monkey.find_one_or_404({"guid": guid})
            monkey_json['config']['exploit_user_list'] = \
                map(lambda x: x['username'], mongo.db.usernames.find({}, {'_id': 0, 'username': 1}).sort([('count', -1)]))
            monkey_json['config']['exploit_password_list'] = \
                map(lambda x: x['password'], mongo.db.passwords.find({}, {'_id': 0, 'password': 1}).sort([('count', -1)]))
            return monkey_json
        else:
            result = {'timestamp': datetime.now().isoformat()}
            find_filter = {}
            if timestamp is not None:
                find_filter['modifytime'] = {'$gt': dateutil.parser.parse(timestamp)}
            result['objects'] = [x for x in mongo.db.monkey.find(find_filter)]
            return result

    def patch(self, guid):
        monkey_json = json.loads(request.data)
        update = {"$set": {'modifytime': datetime.now()}}

        if 'keepalive' in monkey_json:
            update['$set']['keepalive'] = dateutil.parser.parse(monkey_json['keepalive'])
        else:
            update['$set']['keepalive'] = datetime.now()
        if 'config' in monkey_json:
            update['$set']['config'] = monkey_json['config']
        if 'tunnel' in monkey_json:
            update['$set']['tunnel'] = monkey_json['tunnel']
        if 'config_error' in monkey_json:
            update['$set']['config_error'] = monkey_json['config_error']

        return mongo.db.monkey.update({"guid": guid}, update, upsert=False)

    def post(self, **kw):
        monkey_json = json.loads(request.data)
        if 'keepalive' in monkey_json:
            monkey_json['keepalive'] = dateutil.parser.parse(monkey_json['keepalive'])
        else:
            monkey_json['keepalive'] = datetime.now()

        monkey_json['modifytime'] = datetime.now()

        # if new monkey telem, change config according to "new monkeys" config.
        db_monkey = mongo.db.monkey.find_one({"guid": monkey_json["guid"]})
        if not db_monkey:
            new_config = mongo.db.config.find_one({'name': 'newconfig'}) or {}
            monkey_json['config'] = monkey_json.get('config', {})
            monkey_json['config'].update(new_config)
        else:
            db_config = db_monkey.get('config', {})
            if 'current_server' in db_config:
                del db_config['current_server']
            monkey_json.get('config', {}).update(db_config)

        # try to find new monkey parent
        parent = monkey_json.get('parent')
        parent_to_add = (monkey_json.get('guid'), None)  # default values in case of manual run
        if parent and parent != monkey_json.get('guid'):  # current parent is known
            exploit_telem = [x for x in
                             mongo.db.telemetry.find({'telem_type': {'$eq': 'exploit'}, 'data.result': {'$eq': True},
                                                      'data.machine.ip_addr': {'$in': monkey_json['ip_addresses']},
                                                      'monkey_guid': {'$eq': parent}})]
            if 1 == len(exploit_telem):
                parent_to_add = (exploit_telem[0].get('monkey_guid'), exploit_telem[0].get('data').get('exploiter'))
            else:
                parent_to_add = (parent, None)
        elif (not parent or parent == monkey_json.get('guid')) and 'ip_addresses' in  monkey_json:
            exploit_telem = [x for x in
                             mongo.db.telemetry.find({'telem_type': {'$eq': 'exploit'}, 'data.result': {'$eq': True},
                                                      'data.machine.ip_addr': {'$in': monkey_json['ip_addresses']}})]

            if 1 == len(exploit_telem):
                parent_to_add = (exploit_telem[0].get('monkey_guid'), exploit_telem[0].get('data').get('exploiter'))

        if not db_monkey:
            monkey_json['parent'] = [parent_to_add]
        else:
            monkey_json['parent'] = db_monkey.get('parent') + [parent_to_add]

        mongo.db.monkey.update({"guid": monkey_json["guid"]},
                               {"$set": monkey_json},
                               upsert=True)

        # Merge existing scanned node with new monkey

        new_monkey_id = mongo.db.monkey.find_one({"guid": monkey_json["guid"]})["_id"]

        existing_node = mongo.db.node.find_one({"ip_addresses": {"$in": monkey_json["ip_addresses"]}})

        if existing_node:
            id = existing_node["_id"]
            for edge in mongo.db.edge.find({"to": id}):
                mongo.db.edge.update({"_id": edge["_id"]}, {"$set": {"to": new_monkey_id}})
            mongo.db.node.remove({"_id": id})

        return {"id": new_monkey_id}

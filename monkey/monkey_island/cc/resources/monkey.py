import json
from datetime import datetime

import dateutil.parser
import flask_restful
from flask import request

from monkey_island.cc.database import mongo
from monkey_island.cc.models.monkey_ttl import MonkeyTtl
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.node import NodeService

MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS = 60 * 5

__author__ = 'Barak'

# TODO: separate logic from interface


def create_monkey_ttl():
    # The TTL data uses the new `models` module which depends on mongoengine.
    current_ttl = MonkeyTtl.create_ttl_expire_in(MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS)
    current_ttl.save()
    ttlid = current_ttl.id
    return ttlid


class Monkey(flask_restful.Resource):

    # Used by monkey. can't secure.
    def get(self, guid=None, **kw):
        NodeService.update_dead_monkeys()  # refresh monkeys status
        if not guid:
            guid = request.args.get('guid')

        if guid:
            monkey_json = mongo.db.monkey.find_one_or_404({"guid": guid})
            monkey_json['config'] = ConfigService.decrypt_flat_config(monkey_json['config'])
            return monkey_json

        return {}

    # Used by monkey. can't secure.
    def patch(self, guid):
        monkey_json = json.loads(request.data)
        update = {"$set": {'modifytime': datetime.now()}}
        monkey = NodeService.get_monkey_by_guid(guid)
        if 'keepalive' in monkey_json:
            update['$set']['keepalive'] = dateutil.parser.parse(monkey_json['keepalive'])
        else:
            update['$set']['keepalive'] = datetime.now()
        if 'config' in monkey_json:
            update['$set']['config'] = monkey_json['config']
        if 'config_error' in monkey_json:
            update['$set']['config_error'] = monkey_json['config_error']

        if 'tunnel' in monkey_json:
            tunnel_host_ip = monkey_json['tunnel'].split(":")[-2].replace("//", "")
            NodeService.set_monkey_tunnel(monkey["_id"], tunnel_host_ip)

        ttlid = create_monkey_ttl()
        update['$set']['ttl_ref'] = ttlid

        return mongo.db.monkey.update({"_id": monkey["_id"]}, update, upsert=False)

    # Used by monkey. can't secure.
    def post(self, **kw):
        monkey_json = json.loads(request.data)
        monkey_json['creds'] = []
        monkey_json['dead'] = False
        if 'keepalive' in monkey_json:
            monkey_json['keepalive'] = dateutil.parser.parse(monkey_json['keepalive'])
        else:
            monkey_json['keepalive'] = datetime.now()

        monkey_json['modifytime'] = datetime.now()

        ConfigService.save_initial_config_if_needed()

        # if new monkey telem, change config according to "new monkeys" config.
        db_monkey = mongo.db.monkey.find_one({"guid": monkey_json["guid"]})
        if not db_monkey:
            # we pull it encrypted because we then decrypt it for the monkey in get
            new_config = ConfigService.get_flat_config(False, False)
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
                             mongo.db.telemetry.find({'telem_category': {'$eq': 'exploit'}, 'data.result': {'$eq': True},
                                                      'data.machine.ip_addr': {'$in': monkey_json['ip_addresses']},
                                                      'monkey_guid': {'$eq': parent}})]
            if 1 == len(exploit_telem):
                parent_to_add = (exploit_telem[0].get('monkey_guid'), exploit_telem[0].get('data').get('exploiter'))
            else:
                parent_to_add = (parent, None)
        elif (not parent or parent == monkey_json.get('guid')) and 'ip_addresses' in monkey_json:
            exploit_telem = [x for x in
                             mongo.db.telemetry.find({'telem_category': {'$eq': 'exploit'}, 'data.result': {'$eq': True},
                                                      'data.machine.ip_addr': {'$in': monkey_json['ip_addresses']}})]

            if 1 == len(exploit_telem):
                parent_to_add = (exploit_telem[0].get('monkey_guid'), exploit_telem[0].get('data').get('exploiter'))

        if not db_monkey:
            monkey_json['parent'] = [parent_to_add]
        else:
            monkey_json['parent'] = db_monkey.get('parent') + [parent_to_add]

        tunnel_host_ip = None
        if 'tunnel' in monkey_json:
            tunnel_host_ip = monkey_json['tunnel'].split(":")[-2].replace("//", "")
            monkey_json.pop('tunnel')

        monkey_json['ttl_ref'] = create_monkey_ttl()

        mongo.db.monkey.update({"guid": monkey_json["guid"]},
                               {"$set": monkey_json},
                               upsert=True)

        # Merge existing scanned node with new monkey

        new_monkey_id = mongo.db.monkey.find_one({"guid": monkey_json["guid"]})["_id"]

        if tunnel_host_ip is not None:
            NodeService.set_monkey_tunnel(new_monkey_id, tunnel_host_ip)

        existing_node = mongo.db.node.find_one({"ip_addresses": {"$in": monkey_json["ip_addresses"]}})

        if existing_node:
            node_id = existing_node["_id"]
            for edge in mongo.db.edge.find({"to": node_id}):
                mongo.db.edge.update({"_id": edge["_id"]}, {"$set": {"to": new_monkey_id}})
            for creds in existing_node['creds']:
                NodeService.add_credentials_to_monkey(new_monkey_id, creds)
            mongo.db.node.remove({"_id": node_id})

        return {"id": new_monkey_id}

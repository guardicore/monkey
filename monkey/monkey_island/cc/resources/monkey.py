import json
from datetime import datetime

import dateutil.parser
import flask_restful
from flask import request

from monkey_island.cc.consts import \
    DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS
from monkey_island.cc.database import mongo
from monkey_island.cc.models.monkey_ttl import create_monkey_ttl_document
from monkey_island.cc.resources.test.utils.telem_store import TestTelemStore
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.edge.edge import EdgeService
from monkey_island.cc.services.node import NodeService

__author__ = 'Barak'


# TODO: separate logic from interface


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
    @TestTelemStore.store_test_telem
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

        ttl = create_monkey_ttl_document(DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS)
        update['$set']['ttl_ref'] = ttl.id

        return mongo.db.monkey.update({"_id": monkey["_id"]}, update, upsert=False)

    # Used by monkey. can't secure.
    # Called on monkey wakeup to initialize local configuration
    @TestTelemStore.store_test_telem
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

        # Update monkey configuration
        new_config = ConfigService.get_flat_config(False, False)
        monkey_json['config'] = monkey_json.get('config', {})
        monkey_json['config'].update(new_config)

        # try to find new monkey parent
        parent = monkey_json.get('parent')
        parent_to_add = (monkey_json.get('guid'), None)  # default values in case of manual run
        if parent and parent != monkey_json.get('guid'):  # current parent is known
            exploit_telem = [x for x in
                             mongo.db.telemetry.find({'telem_category': {'$eq': 'exploit'},
                                                      'data.result': {'$eq': True},
                                                      'data.machine.ip_addr': {'$in': monkey_json['ip_addresses']},
                                                      'monkey_guid': {'$eq': parent}})]
            if 1 == len(exploit_telem):
                parent_to_add = (exploit_telem[0].get('monkey_guid'), exploit_telem[0].get('data').get('exploiter'))
            else:
                parent_to_add = (parent, None)
        elif (not parent or parent == monkey_json.get('guid')) and 'ip_addresses' in monkey_json:
            exploit_telem = [x for x in
                             mongo.db.telemetry.find({'telem_category': {'$eq': 'exploit'},
                                                      'data.result': {'$eq': True},
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

        ttl = create_monkey_ttl_document(DEFAULT_MONKEY_TTL_EXPIRY_DURATION_IN_SECONDS)
        monkey_json['ttl_ref'] = ttl.id

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
            EdgeService.update_all_dst_nodes(old_dst_node_id=node_id,
                                             new_dst_node_id=new_monkey_id)
            for creds in existing_node['creds']:
                NodeService.add_credentials_to_monkey(new_monkey_id, creds)
            mongo.db.node.remove({"_id": node_id})

        return {"id": new_monkey_id}

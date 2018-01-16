import json
import traceback
import copy
from datetime import datetime

import dateutil
import flask_restful
from flask import request

from cc.database import mongo
from cc.services.config import ConfigService
from cc.services.edge import EdgeService
from cc.services.node import NodeService

__author__ = 'Barak'


class Telemetry(flask_restful.Resource):
    def get(self, **kw):
        monkey_guid = request.args.get('monkey_guid')
        telem_type = request.args.get('telem_type')
        timestamp = request.args.get('timestamp')
        if "null" == timestamp:  # special case to avoid ugly JS code...
            timestamp = None

        result = {'timestamp': datetime.now().isoformat()}
        find_filter = {}

        if monkey_guid:
            find_filter["monkey_guid"] = {'$eq': monkey_guid}
        if telem_type:
            find_filter["telem_type"] = {'$eq': telem_type}
        if timestamp:
            find_filter['timestamp'] = {'$gt': dateutil.parser.parse(timestamp)}

        result['objects'] = self.telemetry_to_displayed_telemetry(mongo.db.telemetry.find(find_filter))
        return result

    def post(self):
        telemetry_json = json.loads(request.data)
        telemetry_json['timestamp'] = datetime.now()

        monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])

        try:
            NodeService.update_monkey_modify_time(monkey["_id"])
            telem_type = telemetry_json.get('telem_type')
            if telem_type in TELEM_PROCESS_DICT:
                TELEM_PROCESS_DICT[telem_type](telemetry_json)
            else:
                print('Got unknown type of telemetry: %s' % telem_type)
        except StandardError as ex:
            print("Exception caught while processing telemetry: %s" % str(ex))
            traceback.print_exc()

        telem_id = mongo.db.telemetry.insert(telemetry_json)
        return mongo.db.telemetry.find_one_or_404({"_id": telem_id})

    @staticmethod
    def telemetry_to_displayed_telemetry(telemetry):
        monkey_guid_dict = {}
        monkeys = mongo.db.monkey.find({})
        for monkey in monkeys:
            monkey_guid_dict[monkey["guid"]] = NodeService.get_monkey_label(monkey)

        objects = []
        for x in telemetry:
            telem_monkey_guid = x.pop("monkey_guid")
            monkey_label = monkey_guid_dict.get(telem_monkey_guid)
            if monkey_label is None:
                monkey_label = telem_monkey_guid
            x["monkey"] = monkey_label
            objects.append(x)
            if x['telem_type'] == 'system_info_collection' and 'credentials' in x['data']:
                for user in x['data']['credentials']:
                    if -1 != user.find(','):
                        new_user = user.replace(',', '.')
                        x['data']['credentials'][new_user] = x['data']['credentials'].pop(user)

        return objects

    @staticmethod
    def get_edge_by_scan_or_exploit_telemetry(telemetry_json):
        dst_ip = telemetry_json['data']['machine']['ip_addr']
        src_monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])
        dst_node = NodeService.get_monkey_by_ip(dst_ip)
        if dst_node is None:
            dst_node = NodeService.get_or_create_node(dst_ip)

        return EdgeService.get_or_create_edge(src_monkey["_id"], dst_node["_id"])

    @staticmethod
    def process_tunnel_telemetry(telemetry_json):
        monkey_id = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])["_id"]
        if telemetry_json['data']['proxy'] is not None:
            tunnel_host_ip = telemetry_json['data']['proxy'].split(":")[-2].replace("//", "")
            NodeService.set_monkey_tunnel(monkey_id, tunnel_host_ip)
        else:
            NodeService.unset_all_monkey_tunnels(monkey_id)

    @staticmethod
    def process_state_telemetry(telemetry_json):
        monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])
        if telemetry_json['data']['done']:
            NodeService.set_monkey_dead(monkey, True)
        else:
            NodeService.set_monkey_dead(monkey, False)

    @staticmethod
    def process_exploit_telemetry(telemetry_json):
        edge = Telemetry.get_edge_by_scan_or_exploit_telemetry(telemetry_json)
        new_exploit = copy.deepcopy(telemetry_json['data'])

        new_exploit.pop('machine')
        new_exploit['timestamp'] = telemetry_json['timestamp']

        mongo.db.edge.update(
            {'_id': edge['_id']},
            {'$push': {'exploits': new_exploit}}
        )
        if new_exploit['result']:
            EdgeService.set_edge_exploited(edge)

        for attempt in telemetry_json['data']['attempts']:
            if attempt['result']:
                attempt.pop('result')
                [attempt.pop(field) for field in ['password', 'lm_hash', 'ntlm_hash'] if len(attempt[field]) == 0]
                NodeService.add_credentials_to_node(edge['to'], attempt)

    @staticmethod
    def process_scan_telemetry(telemetry_json):
        edge = Telemetry.get_edge_by_scan_or_exploit_telemetry(telemetry_json)
        data = copy.deepcopy(telemetry_json['data']['machine'])
        ip_address = data.pop("ip_addr")
        new_scan = \
            {
                "timestamp": telemetry_json["timestamp"],
                "data": data,
                "scanner": telemetry_json['data']['scanner']
            }
        mongo.db.edge.update(
            {"_id": edge["_id"]},
            {"$push": {"scans": new_scan},
             "$set": {"ip_address": ip_address}}
        )

        node = mongo.db.node.find_one({"_id": edge["to"]})
        if node is not None:
            if new_scan["scanner"] == "TcpScanner":
                scan_os = new_scan["data"]["os"]
                if "type" in scan_os:
                    mongo.db.node.update({"_id": node["_id"]},
                                         {"$set": {"os.type": scan_os["type"]}},
                                         upsert=False)
                if "version" in scan_os:
                    mongo.db.node.update({"_id": node["_id"]},
                                         {"$set": {"os.version": scan_os["version"]}},
                                         upsert=False)

    @staticmethod
    def process_system_info_telemetry(telemetry_json):
        if 'credentials' in telemetry_json['data']:
            creds = telemetry_json['data']['credentials']
            for user in creds:
                ConfigService.creds_add_username(user)
                if 'password' in creds[user]:
                    ConfigService.creds_add_password(creds[user]['password'])
                if 'lm_hash' in creds[user]:
                    ConfigService.creds_add_lm_hash(creds[user]['lm_hash'])
                if 'ntlm_hash' in creds[user]:
                    ConfigService.creds_add_ntlm_hash(creds[user]['ntlm_hash'])

            for user in creds:
                if -1 != user.find('.'):
                    new_user = user.replace('.', ',')
                    creds[new_user] = creds.pop(user)

    @staticmethod
    def process_trace_telemetry(telemetry_json):
        # Nothing to do
        return


TELEM_PROCESS_DICT = \
    {
        'tunnel': Telemetry.process_tunnel_telemetry,
        'state': Telemetry.process_state_telemetry,
        'exploit': Telemetry.process_exploit_telemetry,
        'scan': Telemetry.process_scan_telemetry,
        'system_info_collection': Telemetry.process_system_info_telemetry,
        'trace': Telemetry.process_trace_telemetry
    }
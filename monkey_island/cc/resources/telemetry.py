import json
from datetime import datetime
import traceback

import dateutil
from flask import request
import flask_restful

from cc.database import mongo
from cc.services.edge import EdgeService
from cc.services.node import NodeService

from cc.utils import creds_add_username, creds_add_password

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

        result['objects'] = [x for x in mongo.db.telemetry.find(find_filter)]
        return result

    def post(self):
        telemetry_json = json.loads(request.data)
        telemetry_json['timestamp'] = datetime.now()

        telem_id = mongo.db.telemetry.insert(telemetry_json)
        monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])

        try:
            if telemetry_json.get('telem_type') == 'tunnel':
                self.process_tunnel_telemetry(telemetry_json)
            elif telemetry_json.get('telem_type') == 'state':
                self.process_state_telemetry(telemetry_json)
            elif telemetry_json.get('telem_type') in ['scan', 'exploit']:
                self.process_scan_exploit_telemetry(telemetry_json)
            elif telemetry_json.get('telem_type') == 'system_info_collection':
                self.process_system_info_telemetry(telemetry_json)
            NodeService.update_monkey_modify_time(monkey["_id"])
        except StandardError as ex:
            print("Exception caught while processing telemetry: %s" % str(ex))
            traceback.print_exc()

        return mongo.db.telemetry.find_one_or_404({"_id": telem_id})

    def process_tunnel_telemetry(self, telemetry_json):
        monkey_id = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])["_id"]
        NodeService.unset_all_monkey_tunnels(monkey_id)
        if telemetry_json['data']:
            host = telemetry_json['data'].split(":")[-2].replace("//", "")
            tunnel_host_id = NodeService.get_monkey_by_ip(host)["_id"]
            NodeService.set_monkey_tunnel(monkey_id, tunnel_host_id)

    def process_state_telemetry(self, telemetry_json):
        monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])
        if telemetry_json['data']['done']:
            NodeService.set_monkey_dead(monkey, True)
        else:
            NodeService.set_monkey_dead(monkey, False)

    def process_scan_exploit_telemetry(self, telemetry_json):
        dst_ip = telemetry_json['data']['machine']['ip_addr']
        src_monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])
        dst_node = NodeService.get_monkey_by_ip(dst_ip)
        if dst_node is None:
            dst_node = NodeService.get_or_create_node(dst_ip)

        edge = EdgeService.get_or_create_edge(src_monkey["_id"], dst_node["_id"])

        if telemetry_json.get('telem_type') == 'scan':
            self.add_scan_to_edge(edge, telemetry_json)
        else:
            self.add_exploit_to_edge(edge, telemetry_json)

    def process_system_info_telemetry(self, telemetry_json):
        if 'credentials' in telemetry_json['data']:
            creds = telemetry_json['data']['credentials']
            for user in creds:
                creds_add_username(user)

                if 'password' in creds[user]:
                    creds_add_password(creds[user]['password'])

    def add_scan_to_edge(self, edge, telemetry_json):
        data = telemetry_json['data']['machine']
        data.pop("ip_addr")
        new_scan = \
            {
                "timestamp": telemetry_json["timestamp"],
                "data": data,
                "scanner": telemetry_json['data']['scanner']
            }
        mongo.db.edge.update(
            {"_id": edge["_id"]},
            {"$push": {"scans": new_scan}}
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




    def add_exploit_to_edge(self, edge, telemetry_json):
        data = telemetry_json['data']
        data["machine"].pop("ip_addr")
        new_exploit = \
            {
                "timestamp": telemetry_json["timestamp"],
                "data": data,
                "exploiter": telemetry_json['data']['exploiter']
            }
        mongo.db.edge.update(
            {"_id": edge["_id"]},
            {"$push": {"exploits": new_exploit}}
        )


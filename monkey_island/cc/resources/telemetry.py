import json
from datetime import datetime

import dateutil
from flask import request
import flask_restful

from cc.database import mongo

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

        # update exploited monkeys parent
        try:
            if telemetry_json.get('telem_type') == 'tunnel':
                if telemetry_json['data']:
                    host = telemetry_json['data'].split(":")[-2].replace("//", "")
                    tunnel_host = mongo.db.monkey.find_one({"ip_addresses": host})
                    mongo.db.monkey.update({"guid": telemetry_json['monkey_guid']},
                                           {'$set': {'tunnel_guid': tunnel_host.get('guid'),
                                                     'modifytime': datetime.now()}},
                                           upsert=False)
                else:
                    mongo.db.monkey.update({"guid": telemetry_json['monkey_guid']},
                                           {'$unset': {'tunnel_guid': ''},
                                            '$set': {'modifytime': datetime.now()}},
                                           upsert=False)
            elif telemetry_json.get('telem_type') == 'state':
                if telemetry_json['data']['done']:
                    mongo.db.monkey.update({"guid": telemetry_json['monkey_guid']},
                                           {'$set': {'dead': True, 'modifytime': datetime.now()}},
                                           upsert=False)
                else:
                    mongo.db.monkey.update({"guid": telemetry_json['monkey_guid']},
                                           {'$set': {'dead': False, 'modifytime': datetime.now()}},
                                           upsert=False)
            elif telemetry_json.get('telem_type') in ['scan', 'exploit']:
                dst_ip = telemetry_json['data']['machine']['ip_addr']
                src_monkey = mongo.db.monkey.find_one({"guid": telemetry_json['monkey_guid']})
                dst_monkey = mongo.db.monkey.find_one({"ip_addresses": dst_ip})
                if dst_monkey:
                    edge = mongo.db.edge.find_one({"from": src_monkey["_id"], "to": dst_monkey["_id"]})

                    if edge is None:
                        edge = self.insert_edge(src_monkey["_id"], dst_monkey["_id"])

                else:
                    dst_node = mongo.db.node.find_one({"ip_addresses": dst_ip})
                    if dst_node is None:
                        dst_node_insert_result = mongo.db.node.insert_one({"ip_addresses": [dst_ip]})
                        dst_node = mongo.db.node.find_one({"_id": dst_node_insert_result.inserted_id})

                    edge = mongo.db.edge.find_one({"from": src_monkey["_id"], "to": dst_node["_id"]})

                    if edge is None:
                        edge = self.insert_edge(src_monkey["_id"], dst_node["_id"])

                if telemetry_json.get('telem_type') == 'scan':
                    self.add_scan_to_edge(edge, telemetry_json)
                else:
                    self.add_exploit_to_edge(edge, telemetry_json)

        except StandardError as e:
            pass

        # Update credentials DB
        try:
            if (telemetry_json.get('telem_type') == 'system_info_collection') and (telemetry_json['data'].has_key('credentials')):
                creds = telemetry_json['data']['credentials']
                for user in creds:
                    creds_add_username(user)

                    if creds[user].has_key('password'):
                        creds_add_password(creds[user]['password'])
        except StandardError as ex:
            print("Exception caught while updating DB credentials: %s" % str(ex))

        return mongo.db.telemetry.find_one_or_404({"_id": telem_id})

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

    def insert_edge(self, from_id, to_id):
        edge_insert_result = mongo.db.edge.insert_one(
            {
                "from": from_id,
                "to": to_id,
                "scans": [],
                "exploits": []
            })
        return mongo.db.edge.find_one({"_id": edge_insert_result.inserted_id})

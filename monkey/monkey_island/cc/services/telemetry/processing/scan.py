import copy

from monkey_island.cc.database import mongo
from monkey_island.cc.services.telemetry.processing.utils import get_edge_by_scan_or_exploit_telemetry


def process_scan_telemetry(telemetry_json):
    edge = get_edge_by_scan_or_exploit_telemetry(telemetry_json)
    data = copy.deepcopy(telemetry_json['data']['machine'])
    ip_address = data.pop("ip_addr")
    domain_name = data.pop("domain_name")
    new_scan = \
        {
            "timestamp": telemetry_json["timestamp"],
            "data": data
        }
    mongo.db.edge.update(
        {"_id": edge["_id"]},
        {"$push": {"scans": new_scan},
         "$set": {"ip_address": ip_address, 'domain_name': domain_name}}
    )

    node = mongo.db.node.find_one({"_id": edge["to"]})
    if node is not None:
        scan_os = new_scan["data"]["os"]
        if "type" in scan_os:
            mongo.db.node.update({"_id": node["_id"]},
                                 {"$set": {"os.type": scan_os["type"]}},
                                 upsert=False)
        if "version" in scan_os:
            mongo.db.node.update({"_id": node["_id"]},
                                 {"$set": {"os.version": scan_os["version"]}},
                                 upsert=False)

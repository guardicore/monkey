import copy

from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.services.telemetry.processing.utils import get_edge_by_scan_or_exploit_telemetry
from monkey_island.cc.services.telemetry.zero_trust_tests.data_endpoints import test_open_data_endpoints
from monkey_island.cc.services.telemetry.zero_trust_tests.segmentation import test_segmentation_violation


def process_scan_telemetry(telemetry_json):
    update_edges_and_nodes_based_on_scan_telemetry(telemetry_json)
    test_open_data_endpoints(telemetry_json)

    current_monkey = Monkey.get_single_monkey_by_guid(telemetry_json['monkey_guid'])
    target_ip = telemetry_json['data']['machine']['ip_addr']
    test_segmentation_violation(current_monkey, target_ip)


def update_edges_and_nodes_based_on_scan_telemetry(telemetry_json):
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

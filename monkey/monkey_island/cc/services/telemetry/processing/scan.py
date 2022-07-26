from typing import Mapping

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.telemetry.processing.utils import (
    get_edge_by_scan_or_exploit_telemetry,
)
from monkey_island.cc.services.telemetry.zero_trust_checks.data_endpoints import (
    check_open_data_endpoints,
)
from monkey_island.cc.services.telemetry.zero_trust_checks.segmentation import (
    check_segmentation_violation,
)


def process_scan_telemetry(telemetry_json, agent_configuration: AgentConfiguration):
    if not _host_responded(telemetry_json["data"]["machine"]):
        return

    update_edges_and_nodes_based_on_scan_telemetry(telemetry_json)
    check_open_data_endpoints(telemetry_json)

    current_monkey = Monkey.get_single_monkey_by_guid(telemetry_json["monkey_guid"])
    target_ip = telemetry_json["data"]["machine"]["ip_addr"]
    check_segmentation_violation(current_monkey, target_ip, agent_configuration)


def update_edges_and_nodes_based_on_scan_telemetry(telemetry_json):
    edge = get_edge_by_scan_or_exploit_telemetry(telemetry_json)
    edge.update_based_on_scan_telemetry(telemetry_json)

    node = mongo.db.node.find_one({"_id": edge.dst_node_id})
    if node is not None:
        scan_os = telemetry_json["data"]["machine"]["os"]
        if "type" in scan_os:
            mongo.db.node.update(
                {"_id": node["_id"]}, {"$set": {"os.type": scan_os["type"]}}, upsert=False
            )
        if "version" in scan_os:
            mongo.db.node.update(
                {"_id": node["_id"]}, {"$set": {"os.version": scan_os["version"]}}, upsert=False
            )
        label = NodeService.get_label_for_endpoint(node["_id"])
        edge.update_label(node["_id"], label)


def _host_responded(machine_state: Mapping) -> bool:
    return machine_state["icmp"] or _has_open_ports(machine_state)


def _has_open_ports(machine_state: Mapping) -> bool:
    return len(machine_state["services"].keys()) > 0

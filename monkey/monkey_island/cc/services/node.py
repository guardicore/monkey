import socket
from datetime import datetime

from bson import ObjectId

import monkey_island.cc.services.log
from common.network.network_utils import get_my_ip_addresses_legacy
from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.services.edge.displayed_edge import DisplayedEdgeService
from monkey_island.cc.services.edge.edge import EdgeService
from monkey_island.cc.services.utils.node_states import NodeStates


class NodeService:
    def __init__(self):
        pass

    @staticmethod
    def get_displayed_node_by_id(node_id, for_report=False):
        if ObjectId(node_id) == NodeService.get_monkey_island_pseudo_id():
            return NodeService.get_monkey_island_node()

        new_node = {"id": node_id}

        node = NodeService.get_node_by_id(node_id)
        if node is None:
            monkey = NodeService.get_monkey_by_id(node_id)
            if monkey is None:
                return new_node

            # node is infected
            new_node = NodeService.monkey_to_net_node(monkey, for_report)
            for key in monkey:
                if key not in ["_id", "modifytime", "parent", "dead", "description"]:
                    new_node[key] = monkey[key]

        else:
            # node is uninfected
            new_node = NodeService.node_to_net_node(node, for_report)
            new_node["ip_addresses"] = node["ip_addresses"]
            new_node["domain_name"] = node["domain_name"]

        accessible_from_nodes = []
        accessible_from_nodes_hostnames = []
        exploits = []

        edges = DisplayedEdgeService.get_displayed_edges_by_dst(node_id, for_report)

        for edge in edges:
            from_node_id = edge["from"]
            from_node_label = Monkey.get_label_by_id(from_node_id)
            from_node_hostname = Monkey.get_hostname_by_id(from_node_id)

            accessible_from_nodes.append(from_node_label)
            accessible_from_nodes_hostnames.append(from_node_hostname)

            for edge_exploit in edge["exploits"]:
                edge_exploit["origin"] = from_node_label
                exploits.append(edge_exploit)

        exploits = sorted(exploits, key=lambda exploit: exploit["timestamp"])

        new_node["exploits"] = exploits
        new_node["accessible_from_nodes"] = accessible_from_nodes
        new_node["accessible_from_nodes_hostnames"] = accessible_from_nodes_hostnames
        if len(edges) > 0:
            new_node["services"] = edges[-1]["services"]
        else:
            new_node["services"] = []

        new_node["has_log"] = monkey_island.cc.services.log.LogService.log_exists(ObjectId(node_id))
        return new_node

    @staticmethod
    def get_node_label(node):
        domain_name = ""
        if node["domain_name"]:
            domain_name = " (" + node["domain_name"] + ")"
        return node["os"]["version"] + " : " + node["ip_addresses"][0] + domain_name

    # A lot of methods like these duplicate between monkey and node.
    # That's a result of poor entity model, because both nodes and monkeys
    # store the same information. It's best to extract the machine specific data
    # to "Machine" entity (like IP's and os) and agent specific data to "Agent" (like alive,
    # parent, etc)
    @staticmethod
    def get_monkey_os(monkey):
        os = "unknown"
        if monkey["description"].lower().find("linux") != -1:
            os = "linux"
        elif monkey["description"].lower().find("windows") != -1:
            os = "windows"
        return os

    @staticmethod
    def get_node_os(node):
        return node["os"]["type"]

    @staticmethod
    def get_monkey_manual_run(monkey):
        for p in monkey["parent"]:
            if p[0] != monkey["guid"]:
                return False

        return True

    @staticmethod
    def get_monkey_label(monkey):
        # todo
        label = monkey["hostname"] + " : " + monkey["ip_addresses"][0]
        ip_addresses = get_my_ip_addresses_legacy()
        if len(set(monkey["ip_addresses"]).intersection(ip_addresses)) > 0:
            label = "MonkeyIsland - " + label
        return label

    @staticmethod
    def get_monkey_group(monkey):
        keywords = []
        if len(set(monkey["ip_addresses"]).intersection(get_my_ip_addresses_legacy())) != 0:
            keywords.extend(["island", "monkey"])
        else:
            monkey_type = "manual" if NodeService.get_monkey_manual_run(monkey) else "monkey"
            keywords.append(monkey_type)

        keywords.append(NodeService.get_monkey_os(monkey))
        if not Monkey.get_single_monkey_by_id(monkey["_id"]).is_dead():
            keywords.append("running")
        return NodeStates.get_by_keywords(keywords).value

    @staticmethod
    def get_node_group(node) -> str:
        if "group" in node and node["group"]:
            return node["group"]

        if node.get("propagated"):
            node_type = "propagated"
        else:
            node_type = "clean"

        node_os = NodeService.get_node_os(node)

        return NodeStates.get_by_keywords([node_type, node_os]).value

    @staticmethod
    def monkey_to_net_node(monkey, for_report=False):
        monkey_id = monkey["_id"]
        label = (
            Monkey.get_hostname_by_id(monkey_id)
            if for_report
            else Monkey.get_label_by_id(monkey_id)
        )
        monkey_group = NodeService.get_monkey_group(monkey)
        return {
            "id": monkey_id,
            "label": label,
            "group": monkey_group,
            "os": NodeService.get_monkey_os(monkey),
            # The monkey is running IFF the group contains "_running". Therefore it's dead IFF
            # the group does NOT
            # contain "_running". This is a small optimisation, to not call "is_dead" twice.
            "dead": "_running" not in monkey_group,
            "domain_name": "",
            "pba_results": monkey["pba_results"] if "pba_results" in monkey else [],
        }

    @staticmethod
    def node_to_net_node(node, for_report=False):
        label = node["os"]["version"] if for_report else NodeService.get_node_label(node)
        return {
            "id": node["_id"],
            "label": label,
            "group": NodeService.get_node_group(node),
            "os": NodeService.get_node_os(node),
        }

    @staticmethod
    def unset_all_monkey_tunnels(monkey_id):
        mongo.db.monkey.update({"_id": monkey_id}, {"$unset": {"tunnel": ""}}, upsert=False)

        edges = EdgeService.get_tunnel_edges_by_src(monkey_id)
        for edge in edges:
            edge.disable_tunnel()

    @staticmethod
    def set_monkey_tunnel(monkey_id, tunnel_host_ip):
        tunnel_host_id = NodeService.get_monkey_by_ip(tunnel_host_ip)["_id"]
        NodeService.unset_all_monkey_tunnels(monkey_id)
        mongo.db.monkey.update(
            {"_id": monkey_id}, {"$set": {"tunnel": tunnel_host_id}}, upsert=False
        )
        monkey_label = NodeService.get_label_for_endpoint(monkey_id)
        tunnel_host_label = NodeService.get_label_for_endpoint(tunnel_host_id)
        tunnel_edge = EdgeService.get_or_create_edge(
            src_node_id=monkey_id,
            dst_node_id=tunnel_host_id,
            src_label=monkey_label,
            dst_label=tunnel_host_label,
        )
        tunnel_edge.tunnel = True
        tunnel_edge.ip_address = tunnel_host_ip
        tunnel_edge.save()

    @staticmethod
    def get_monkey_by_id(monkey_id):
        return mongo.db.monkey.find_one({"_id": ObjectId(monkey_id)})

    # GUID is generated from uuid.getnode() and represents machine it was ran on
    # All monkeys that ran on the same machine will have the same GUID, but
    # we can just store the monkeys on the same machine document/have one to many relationship
    # GUID could be stored on machine to uniquely identify the same machine even after the
    # ip, domain name or other changes. Not entirely sure it's necessary
    @staticmethod
    def get_monkey_by_guid(monkey_guid):
        return mongo.db.monkey.find_one({"guid": monkey_guid})

    @staticmethod
    def get_monkey_by_ip(ip_address):
        return mongo.db.monkey.find_one({"ip_addresses": ip_address})

    @staticmethod
    def get_node_by_id(node_id):
        return mongo.db.node.find_one({"_id": ObjectId(node_id)})

    # This is only used to determine if report is the latest or if we need to
    # generate a new one. This info should end up in Simulation entity instead.
    @staticmethod
    def update_monkey_modify_time(monkey_id):
        mongo.db.monkey.update(
            {"_id": monkey_id}, {"$set": {"modifytime": datetime.now()}}, upsert=False
        )

    @staticmethod
    def set_monkey_dead(monkey, is_dead):
        props_to_set = {"dead": is_dead}

        # Cancel the force kill once monkey died
        if is_dead:
            props_to_set["should_stop"] = False

        mongo.db.monkey.update({"guid": monkey["guid"]}, {"$set": props_to_set}, upsert=False)

    @staticmethod
    def add_communication_info(monkey, info):
        mongo.db.monkey.update(
            {"guid": monkey["guid"]}, {"$set": {"command_control_channel": info}}, upsert=False
        )

    # TODO this returns a mock island agent
    # It's better to just initialize the island machine on reset I think
    @staticmethod
    def get_monkey_island_monkey():
        ip_addresses = get_my_ip_addresses_legacy()
        for ip_address in ip_addresses:
            monkey = NodeService.get_monkey_by_ip(ip_address)
            if monkey is not None:
                return monkey
        return None

    @staticmethod
    def get_monkey_island_pseudo_id():
        return ObjectId("000000000000000000000000")

    @staticmethod
    def get_monkey_island_pseudo_net_node():
        return {
            "id": NodeService.get_monkey_island_pseudo_id(),
            "label": "MonkeyIsland",
            "group": "island",
        }

    @staticmethod
    def get_monkey_island_node():
        island_node = NodeService.get_monkey_island_pseudo_net_node()
        island_node["ip_addresses"] = get_my_ip_addresses_legacy()
        island_node["domain_name"] = socket.gethostname()
        return island_node

    @staticmethod
    def get_node_or_monkey_by_id(node_id):
        node = NodeService.get_node_by_id(node_id)
        if node is not None:
            return node
        return NodeService.get_monkey_by_id(node_id)

    @staticmethod
    def get_node_hostname(node):
        return node["hostname"] if "hostname" in node else node["os"]["version"]

    @staticmethod
    def get_hostname_by_id(node_id):
        return NodeService.get_node_hostname(
            mongo.db.monkey.find_one({"_id": node_id}, {"hostname": 1})
        )

    @staticmethod
    def get_label_for_endpoint(endpoint_id):
        if endpoint_id == ObjectId("000000000000000000000000"):
            return "MonkeyIsland"
        if Monkey.is_monkey(endpoint_id):
            return Monkey.get_label_by_id(endpoint_id)
        else:
            return NodeService.get_node_label(NodeService.get_node_by_id(endpoint_id))

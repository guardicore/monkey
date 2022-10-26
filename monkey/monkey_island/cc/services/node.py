from datetime import datetime

from bson import ObjectId

from common.network.network_utils import get_my_ip_addresses_legacy
from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.services.edge.edge import EdgeService


class NodeService:
    def __init__(self):
        pass

    @staticmethod
    def get_node_label(node):
        domain_name = ""
        if node["domain_name"]:
            domain_name = " (" + node["domain_name"] + ")"
        return node["os"]["version"] + " : " + node["ip_addresses"][0] + domain_name

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

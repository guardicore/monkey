from datetime import datetime, timedelta
from bson import ObjectId

from cc.database import mongo
from cc.services.edge import EdgeService
from cc.utils import local_ip_addresses
__author__ = "itay.mizeretz"


class NodeService:
    def __init__(self):
        pass

    @staticmethod
    def get_displayed_node_by_id(node_id, for_report=False):
        if ObjectId(node_id) == NodeService.get_monkey_island_pseudo_id():
            return NodeService.get_monkey_island_node()

        edges = EdgeService.get_displayed_edges_by_to(node_id, for_report)
        accessible_from_nodes = []
        exploits = []

        new_node = {"id": node_id}

        node = NodeService.get_node_by_id(node_id)
        if node is None:
            monkey = NodeService.get_monkey_by_id(node_id)
            if monkey is None:
                return new_node

            # node is infected
            new_node = NodeService.monkey_to_net_node(monkey, for_report)
            for key in monkey:
                if key not in ['_id', 'modifytime', 'parent', 'dead', 'description']:
                    new_node[key] = monkey[key]

        else:
            # node is uninfected
            new_node = NodeService.node_to_net_node(node, for_report)
            new_node["ip_addresses"] = node["ip_addresses"]

        for edge in edges:
            accessible_from_nodes.append(NodeService.get_monkey_label(NodeService.get_monkey_by_id(edge["from"])))
            for exploit in edge["exploits"]:
                exploit["origin"] = NodeService.get_monkey_label(NodeService.get_monkey_by_id(edge["from"]))
                exploits.append(exploit)

        exploits.sort(cmp=NodeService._cmp_exploits_by_timestamp)

        new_node["exploits"] = exploits
        new_node["accessible_from_nodes"] = accessible_from_nodes
        if len(edges) > 0:
            new_node["services"] = edges[-1]["services"]
        else:
            new_node["services"] = []

        return new_node

    @staticmethod
    def get_node_label(node):
        return node["os"]["version"] + " : " + node["ip_addresses"][0]

    @staticmethod
    def _cmp_exploits_by_timestamp(exploit_1, exploit_2):
        if exploit_1["timestamp"] == exploit_2["timestamp"]:
            return 0
        if exploit_1["timestamp"] > exploit_2["timestamp"]:
            return 1
        return -1

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
    def get_monkey_label_by_id(monkey_id):
        return NodeService.get_monkey_label(NodeService.get_monkey_by_id(monkey_id))

    @staticmethod
    def get_monkey_label(monkey):
        label = monkey["hostname"] + " : " + monkey["ip_addresses"][0]
        ip_addresses = local_ip_addresses()
        if len(set(monkey["ip_addresses"]).intersection(ip_addresses)) > 0:
            label = "MonkeyIsland - " + label
        return label

    @staticmethod
    def get_monkey_group(monkey):
        if len(set(monkey["ip_addresses"]).intersection(local_ip_addresses())) != 0:
            monkey_type = "island_monkey"
        else:
            monkey_type = "manual" if NodeService.get_monkey_manual_run(monkey) else "monkey"

        monkey_os = NodeService.get_monkey_os(monkey)
        monkey_running = "" if monkey["dead"] else "_running"
        return "%s_%s%s" % (monkey_type, monkey_os, monkey_running)

    @staticmethod
    def get_node_group(node):
        node_type = "exploited" if node.get("exploited") else "clean"
        node_os = NodeService.get_node_os(node)
        return "%s_%s" % (node_type, node_os)

    @staticmethod
    def monkey_to_net_node(monkey, for_report=False):
        label = monkey['hostname'] if for_report else NodeService.get_monkey_label(monkey)
        return \
            {
                "id": monkey["_id"],
                "label": label,
                "group": NodeService.get_monkey_group(monkey),
                "os": NodeService.get_monkey_os(monkey),
                "dead": monkey["dead"],
            }

    @staticmethod
    def node_to_net_node(node, for_report=False):
        label = node['os']['version'] if for_report else NodeService.get_node_label(node)
        return \
            {
                "id": node["_id"],
                "label": label,
                "group": NodeService.get_node_group(node),
                "os": NodeService.get_node_os(node)
            }

    @staticmethod
    def unset_all_monkey_tunnels(monkey_id):
        mongo.db.monkey.update(
            {"_id": monkey_id},
            {'$unset': {'tunnel': ''}},
            upsert=False)

        mongo.db.edge.update(
            {"from": monkey_id, 'tunnel': True},
            {'$set': {'tunnel': False}},
            upsert=False)

    @staticmethod
    def set_monkey_tunnel(monkey_id, tunnel_host_ip):
        tunnel_host_id = NodeService.get_monkey_by_ip(tunnel_host_ip)["_id"]
        NodeService.unset_all_monkey_tunnels(monkey_id)
        mongo.db.monkey.update(
            {"_id": monkey_id},
            {'$set': {'tunnel': tunnel_host_id}},
            upsert=False)
        tunnel_edge = EdgeService.get_or_create_edge(monkey_id, tunnel_host_id)
        mongo.db.edge.update({"_id": tunnel_edge["_id"]},
                             {'$set': {'tunnel': True, 'ip_address': tunnel_host_ip}},
                             upsert=False)

    @staticmethod
    def insert_node(ip_address):
        new_node_insert_result = mongo.db.node.insert_one(
            {
                "ip_addresses": [ip_address],
                "exploited": False,
                "creds": [],
                "os":
                    {
                        "type": "unknown",
                        "version": "unknown"
                    }
            })
        return mongo.db.node.find_one({"_id": new_node_insert_result.inserted_id})

    @staticmethod
    def get_or_create_node(ip_address):
        new_node = mongo.db.node.find_one({"ip_addresses": ip_address})
        if new_node is None:
            new_node = NodeService.insert_node(ip_address)
        return new_node

    @staticmethod
    def get_monkey_by_id(monkey_id):
        return mongo.db.monkey.find_one({"_id": ObjectId(monkey_id)})

    @staticmethod
    def get_monkey_by_guid(monkey_guid):
        return mongo.db.monkey.find_one({"guid": monkey_guid})

    @staticmethod
    def get_monkey_by_ip(ip_address):
        return mongo.db.monkey.find_one({"ip_addresses": ip_address})

    @staticmethod
    def get_node_by_ip(ip_address):
        return mongo.db.node.find_one({"ip_addresses": ip_address})

    @staticmethod
    def get_node_by_id(node_id):
        return mongo.db.node.find_one({"_id": ObjectId(node_id)})

    @staticmethod
    def update_monkey_modify_time(monkey_id):
        mongo.db.monkey.update({"_id": monkey_id},
                               {"$set": {"modifytime": datetime.now()}},
                               upsert=False)

    @staticmethod
    def set_monkey_dead(monkey, is_dead):
        props_to_set = {'dead': is_dead}

        # Cancel the force kill once monkey died
        if is_dead:
            props_to_set['config.alive'] = True

        mongo.db.monkey.update({"guid": monkey['guid']},
                               {'$set': props_to_set},
                               upsert=False)

    @staticmethod
    def get_monkey_island_monkey():
        ip_addresses = local_ip_addresses()
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
        return\
            {
                "id": NodeService.get_monkey_island_pseudo_id(),
                "label": "MonkeyIsland",
                "group": "island",
            }

    @staticmethod
    def get_monkey_island_node():
        island_node = NodeService.get_monkey_island_pseudo_net_node()
        island_node["ip_addresses"] = local_ip_addresses()
        return island_node

    @staticmethod
    def set_node_exploited(node_id):
        mongo.db.node.update(
            {"_id": node_id},
            {"$set": {"exploited": True}}
        )

    @staticmethod
    def update_dead_monkeys():
        # Update dead monkeys only if no living monkey transmitted keepalive in the last 10 minutes
        if mongo.db.monkey.find_one(
                {'dead': {'$ne': True}, 'keepalive': {'$gte': datetime.now() - timedelta(minutes=10)}}):
            return

        # config.alive is changed to true to cancel the force kill of dead monkeys
        mongo.db.monkey.update(
            {'keepalive': {'$lte': datetime.now() - timedelta(minutes=10)}, 'dead': {'$ne': True}},
            {'$set': {'dead': True, 'config.alive': True, 'modifytime': datetime.now()}}, upsert=False, multi=True)

    @staticmethod
    def is_any_monkey_alive():
        return mongo.db.monkey.find_one({'dead': False}) is not None

    @staticmethod
    def is_any_monkey_exists():
        return mongo.db.monkey.find_one({}) is not None

    @staticmethod
    def is_monkey_finished_running():
        return NodeService.is_any_monkey_exists() and not NodeService.is_any_monkey_alive()

    @staticmethod
    def add_credentials_to_monkey(monkey_id, creds):
        mongo.db.monkey.update(
            {'_id': monkey_id},
            {'$push': {'creds': creds}}
        )

    @staticmethod
    def add_credentials_to_node(node_id, creds):
        mongo.db.node.update(
            {'_id': node_id},
            {'$push': {'creds': creds}}
        )

    @staticmethod
    def get_node_or_monkey_by_ip(ip_address):
        node = NodeService.get_node_by_ip(ip_address)
        if node is not None:
            return node
        return NodeService.get_monkey_by_ip(ip_address)

    @staticmethod
    def get_node_or_monkey_by_id(node_id):
        node = NodeService.get_node_by_id(node_id)
        if node is not None:
            return node
        return NodeService.get_monkey_by_id(node_id)

    @staticmethod
    def get_node_hostname(node):
        return node['hostname'] if 'hostname' in node else node['os']['version']

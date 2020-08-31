import socket
from datetime import datetime, timedelta
from typing import Dict

from bson import ObjectId

import monkey_island.cc.services.log
from monkey_island.cc import models
from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.network_utils import is_local_ips, local_ip_addresses
from monkey_island.cc.services.edge.displayed_edge import DisplayedEdgeService
from monkey_island.cc.services.edge.edge import EdgeService
from monkey_island.cc.services.utils.node_states import NodeStates

__author__ = "itay.mizeretz"


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
                if key not in ['_id', 'modifytime', 'parent', 'dead', 'description']:
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
            from_node_id = edge['from']
            from_node_label = Monkey.get_label_by_id(from_node_id)
            from_node_hostname = Monkey.get_hostname_by_id(from_node_id)

            accessible_from_nodes.append(from_node_label)
            accessible_from_nodes_hostnames.append(from_node_hostname)

            for edge_exploit in edge['exploits']:
                edge_exploit['origin'] = from_node_label
                exploits.append(edge_exploit)

        exploits = sorted(exploits, key=lambda exploit: exploit['timestamp'])

        new_node["exploits"] = exploits
        new_node["accessible_from_nodes"] = accessible_from_nodes
        new_node["accessible_from_nodes_hostnames"] = accessible_from_nodes_hostnames
        if len(edges) > 0:
            new_node["services"] = edges[-1]["services"]
        else:
            new_node["services"] = []

        new_node['has_log'] = monkey_island.cc.services.log.LogService.log_exists(ObjectId(node_id))
        return new_node

    @staticmethod
    def get_node_label(node):
        domain_name = ""
        if node["domain_name"]:
            domain_name = " (" + node["domain_name"] + ")"
        return node["os"]["version"] + " : " + node["ip_addresses"][0] + domain_name

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
    def get_monkey_critical_services(monkey_id):
        critical_services = mongo.db.monkey.find_one({'_id': monkey_id}, {'critical_services': 1}).get(
            'critical_services', [])
        return critical_services

    @staticmethod
    def get_monkey_label(monkey):
        # todo
        label = monkey["hostname"] + " : " + monkey["ip_addresses"][0]
        ip_addresses = local_ip_addresses()
        if len(set(monkey["ip_addresses"]).intersection(ip_addresses)) > 0:
            label = "MonkeyIsland - " + label
        return label

    @staticmethod
    def get_monkey_group(monkey):
        keywords = []
        if len(set(monkey["ip_addresses"]).intersection(local_ip_addresses())) != 0:
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
        if 'group' in node and node['group']:
            return node['group']
        node_type = "exploited" if node.get("exploited") else "clean"
        node_os = NodeService.get_node_os(node)
        return NodeStates.get_by_keywords([node_type, node_os]).value

    @staticmethod
    def monkey_to_net_node(monkey, for_report=False):
        monkey_id = monkey["_id"]
        label = Monkey.get_hostname_by_id(monkey_id) if for_report else Monkey.get_label_by_id(monkey_id)
        monkey_group = NodeService.get_monkey_group(monkey)
        return \
            {
                "id": monkey_id,
                "label": label,
                "group": monkey_group,
                "os": NodeService.get_monkey_os(monkey),
                # The monkey is running IFF the group contains "_running". Therefore it's dead IFF the group does NOT
                # contain "_running". This is a small optimisation, to not call "is_dead" twice.
                "dead": "_running" not in monkey_group,
                "domain_name": "",
                "pba_results": monkey["pba_results"] if "pba_results" in monkey else []
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
    def set_node_group(node_id: str, node_group: NodeStates):
        mongo.db.node.update({"_id": node_id},
                             {'$set': {'group': node_group.value}},
                             upsert=False)

    @staticmethod
    def unset_all_monkey_tunnels(monkey_id):
        mongo.db.monkey.update(
            {"_id": monkey_id},
            {'$unset': {'tunnel': ''}},
            upsert=False)

        edges = EdgeService.get_tunnel_edges_by_src(monkey_id)
        for edge in edges:
            edge.disable_tunnel()

    @staticmethod
    def set_monkey_tunnel(monkey_id, tunnel_host_ip):
        tunnel_host_id = NodeService.get_monkey_by_ip(tunnel_host_ip)["_id"]
        NodeService.unset_all_monkey_tunnels(monkey_id)
        mongo.db.monkey.update(
            {'_id': monkey_id},
            {'$set': {'tunnel': tunnel_host_id}},
            upsert=False)
        monkey_label = NodeService.get_label_for_endpoint(monkey_id)
        tunnel_host_label = NodeService.get_label_for_endpoint(tunnel_host_id)
        tunnel_edge = EdgeService.get_or_create_edge(src_node_id=monkey_id,
                                                     dst_node_id=tunnel_host_id,
                                                     src_label=monkey_label,
                                                     dst_label=tunnel_host_label)
        tunnel_edge.tunnel = True
        tunnel_edge.ip_address = tunnel_host_ip
        tunnel_edge.save()

    @staticmethod
    def insert_node(ip_address, domain_name=''):
        new_node_insert_result = mongo.db.node.insert_one(
            {
                "ip_addresses": [ip_address],
                "domain_name": domain_name,
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
    def create_node_from_bootloader_telem(bootloader_telem: Dict, will_monkey_run: bool):
        new_node_insert_result = mongo.db.node.insert_one(
            {
                "ip_addresses": bootloader_telem['ips'],
                "domain_name": bootloader_telem['hostname'],
                "will_monkey_run": will_monkey_run,
                "exploited": False,
                "creds": [],
                "os":
                    {
                        "type": bootloader_telem['system'],
                        "version": bootloader_telem['os_version']
                    }
            })
        return mongo.db.node.find_one({"_id": new_node_insert_result.inserted_id})

    @staticmethod
    def get_or_create_node_from_bootloader_telem(bootloader_telem: Dict, will_monkey_run: bool) -> Dict:
        if is_local_ips(bootloader_telem['ips']):
            raise NodeCreationException("Bootloader ran on island, no need to create new node.")

        new_node = mongo.db.node.find_one({"ip_addresses": {"$in": bootloader_telem['ips']}})
        # Temporary workaround to not create a node after monkey finishes
        monkey_node = mongo.db.monkey.find_one({"ip_addresses": {"$in": bootloader_telem['ips']}})
        if monkey_node:
            # Don't create new node, monkey node is already present
            return monkey_node

        if new_node is None:
            new_node = NodeService.create_node_from_bootloader_telem(bootloader_telem, will_monkey_run)
            if bootloader_telem['tunnel']:
                dst_node = NodeService.get_node_or_monkey_by_ip(bootloader_telem['tunnel'])
            else:
                dst_node = NodeService.get_monkey_island_node()
            src_label = NodeService.get_label_for_endpoint(new_node['_id'])
            dst_label = NodeService.get_label_for_endpoint(dst_node['id'])
            edge = EdgeService.get_or_create_edge(src_node_id=new_node['_id'],
                                                  dst_node_id=dst_node['id'],
                                                  src_label=src_label,
                                                  dst_label=dst_label)
            edge.tunnel = bool(bootloader_telem['tunnel'])
            edge.ip_address = bootloader_telem['ips'][0]
            edge.group = NodeStates.get_by_keywords(['island']).value
            edge.save()
        return new_node

    @staticmethod
    def get_or_create_node(ip_address, domain_name=''):
        new_node = mongo.db.node.find_one({"ip_addresses": ip_address})
        if new_node is None:
            new_node = NodeService.insert_node(ip_address, domain_name)
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
    def add_communication_info(monkey, info):
        mongo.db.monkey.update({"guid": monkey["guid"]},
                               {"$set": {'command_control_channel': info}},
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
        return \
            {
                "id": NodeService.get_monkey_island_pseudo_id(),
                "label": "MonkeyIsland",
                "group": "island",
            }

    @staticmethod
    def get_monkey_island_node():
        island_node = NodeService.get_monkey_island_pseudo_net_node()
        island_node["ip_addresses"] = local_ip_addresses()
        island_node["domain_name"] = socket.gethostname()
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
        all_monkeys = models.Monkey.objects()
        return any(not monkey.is_dead() for monkey in all_monkeys)

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

    @staticmethod
    def get_hostname_by_id(node_id):
        return NodeService.get_node_hostname(mongo.db.monkey.find_one({'_id': node_id}, {'hostname': 1}))

    @staticmethod
    def get_label_for_endpoint(endpoint_id):
        if endpoint_id == ObjectId("000000000000000000000000"):
            return 'MonkeyIsland'
        if Monkey.is_monkey(endpoint_id):
            return Monkey.get_label_by_id(endpoint_id)
        else:
            return NodeService.get_node_label(NodeService.get_node_by_id(endpoint_id))


class NodeCreationException(Exception):
    pass

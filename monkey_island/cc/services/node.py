from bson import ObjectId

from cc.database import mongo
from cc.services.edge import EdgeService

__author__ = "itay.mizeretz"


class NodeService:

    @staticmethod
    def get_displayed_node_by_id(node_id):

        edges = EdgeService.get_displayed_edges_by_to(node_id)
        accessible_from_nodes = []
        exploits = []

        new_node = {"id": node_id}

        node = mongo.db.node.find_one({"_id": ObjectId(node_id)})
        if node is None:
            monkey = mongo.db.monkey.find_one({"_id": ObjectId(node_id)})
            if monkey is None:
                return new_node

            # node is infected
            for key in monkey:
                # TODO: do something with tunnel
                if key not in ["_id", "modifytime", "parent", "tunnel", "tunnel_guid"]:
                    new_node[key] = monkey[key]

            new_node["os"] = NodeService.get_monkey_os(monkey)
            new_node["label"] = NodeService.get_monkey_label(monkey)
            new_node["group"] = NodeService.get_monkey_group(monkey)

        else:
            # node is uninfected
            new_node["ip_addresses"] = node["ip_addresses"]
            new_node["group"] = "clean"

        for edge in edges:
            accessible_from_nodes.append({"id": edge["from"]})
            for exploit in edge["exploits"]:
                exploit["origin"] = edge["from"]
                exploits.append(exploit)

        exploits.sort(cmp=NodeService._cmp_exploits_by_timestamp)

        new_node["exploits"] = exploits
        new_node["accessible_from_nodes"] = accessible_from_nodes
        if len(edges) > 0:
            new_node["services"] = edges[-1]["services"]
            new_node["os"] = edges[-1]["os"]["type"]
            if "label" not in new_node:
                new_node["label"] = edges[-1]["os"]["version"] + " : " + node["ip_addresses"][0]

        # TODO: add exploited by

        return new_node

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
    def get_monkey_manual_run(monkey):
        # TODO: find better implementation
        return monkey["parent"][0][1] == None

    @staticmethod
    def get_monkey_label(monkey):
        return monkey["hostname"] + " : " + monkey["ip_addresses"][0]

    @staticmethod
    def get_monkey_group(monkey):
        return "manuallyInfected" if NodeService.get_monkey_manual_run(monkey) else "infected"

    @staticmethod
    def monkey_to_net_node(monkey):
        return \
            {
                "id": monkey["_id"],
                "label": NodeService.get_monkey_label(monkey),
                "group": NodeService.get_monkey_group(monkey),
                "os": NodeService.get_monkey_os(monkey),
                "dead": monkey["dead"],
            }

    @staticmethod
    def node_to_net_node(node):
        os_version = "undefined"
        os_type = "undefined"
        found = False
        # TODO: Set this as data when received
        for edge in mongo.db.edge.find({"to": node["_id"]}):
            for scan in edge["scans"]:
                if scan["scanner"] != "TcpScanner":
                    continue
                os_type = scan["data"]["os"]["type"]
                if "version" in scan["data"]["os"]:
                    os_version = scan["data"]["os"]["version"]
                    found = True
                    break
            if found:
                break

        return \
            {
                "id": node["_id"],
                "label": os_version + " : " + node["ip_addresses"][0],
                "group": "clean",
                "os": os_type
            }
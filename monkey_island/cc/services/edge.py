from bson import ObjectId

from cc.database import mongo
import cc.services.node

__author__ = "itay.mizeretz"


class EdgeService:
    def __init__(self):
        pass

    @staticmethod
    def get_displayed_edge_by_id(edge_id, for_report=False):
        edge = mongo.db.edge.find({"_id": ObjectId(edge_id)})[0]
        return EdgeService.edge_to_displayed_edge(edge, for_report)

    @staticmethod
    def get_displayed_edges_by_to(to, for_report=False):
        edges = mongo.db.edge.find({"to": ObjectId(to)})
        return [EdgeService.edge_to_displayed_edge(edge, for_report) for edge in edges]

    @staticmethod
    def edge_to_displayed_edge(edge, for_report=False):
        services = []
        os = {}

        if len(edge["scans"]) > 0:
            services = EdgeService.services_to_displayed_services(edge["scans"][-1]["data"]["services"], for_report)
            os = edge["scans"][-1]["data"]["os"]

        displayed_edge = EdgeService.edge_to_net_edge(edge)

        displayed_edge["ip_address"] = edge["ip_address"]
        displayed_edge["services"] = services
        displayed_edge["os"] = os
        displayed_edge["exploits"] = edge['exploits']
        displayed_edge["_label"] = EdgeService.get_edge_label(displayed_edge)
        return displayed_edge

    @staticmethod
    def insert_edge(from_id, to_id):
        edge_insert_result = mongo.db.edge.insert_one(
            {
                "from": from_id,
                "to": to_id,
                "scans": [],
                "exploits": [],
                "tunnel": False,
                "exploited": False
            })
        return mongo.db.edge.find_one({"_id": edge_insert_result.inserted_id})

    @staticmethod
    def get_or_create_edge(edge_from, edge_to):
        tunnel_edge = mongo.db.edge.find_one({"from": edge_from, "to": edge_to})
        if tunnel_edge is None:
            tunnel_edge = EdgeService.insert_edge(edge_from, edge_to)

        return tunnel_edge

    @staticmethod
    def generate_pseudo_edge(edge_id, edge_from, edge_to):
        edge = \
            {
                "id": edge_id,
                "from": edge_from,
                "to": edge_to,
                "group": "island"
            }
        edge["_label"] = EdgeService.get_edge_label(edge)
        return edge

    @staticmethod
    def get_monkey_island_pseudo_edges():
        edges = []
        monkey_ids = [x["_id"] for x in mongo.db.monkey.find({}) if "tunnel" not in x]
        # We're using fake ids because the frontend graph module requires unique ids.
        # Collision with real id is improbable.
        count = 0
        for monkey_id in monkey_ids:
            count += 1
            edges.append(EdgeService.generate_pseudo_edge(
                ObjectId(hex(count)[2:].zfill(24)), monkey_id, ObjectId("000000000000000000000000")))

        return edges

    @staticmethod
    def get_infected_monkey_island_pseudo_edges():
        monkey = cc.services.node.NodeService.get_monkey_island_monkey()
        existing_ids = [x["from"] for x in mongo.db.edge.find({"to": monkey["_id"]})]
        monkey_ids = [x["_id"] for x in mongo.db.monkey.find({})
                      if ("tunnel" not in x) and (x["_id"] not in existing_ids) and (x["_id"] != monkey["_id"])]
        edges = []

        # We're using fake ids because the frontend graph module requires unique ids.
        # Collision with real id is improbable.
        count = 0
        for monkey_id in monkey_ids:
            count += 1
            edges.append(EdgeService.generate_pseudo_edge(
                ObjectId(hex(count)[2:].zfill(24)), monkey_id, monkey["_id"]))

        return edges

    @staticmethod
    def services_to_displayed_services(services, for_report=False):
        if for_report:
            return [x for x in services]
        else:
            return [x + ": " + (services[x]['name'] if 'name' in services[x] else 'unknown') for x in services]

    @staticmethod
    def edge_to_net_edge(edge):
        return \
            {
                "id": edge["_id"],
                "from": edge["from"],
                "to": edge["to"],
                "group": EdgeService.get_edge_group(edge)
            }

    @staticmethod
    def get_edge_group(edge):
        if edge.get("exploited"):
            return "exploited"
        if edge.get("tunnel"):
            return "tunnel"
        if (len(edge.get("scans", [])) > 0) or (len(edge.get("exploits", [])) > 0):
            return "scan"
        return "empty"

    @staticmethod
    def set_edge_exploited(edge):
        mongo.db.edge.update(
            {"_id": edge["_id"]},
            {"$set": {"exploited": True}}
        )
        cc.services.node.NodeService.set_node_exploited(edge["to"])

    @staticmethod
    def get_edge_label(edge):
        NodeService = cc.services.node.NodeService
        from_label = NodeService.get_monkey_label(NodeService.get_monkey_by_id(edge["from"]))
        if edge["to"] == ObjectId("000000000000000000000000"):
            to_label = 'MonkeyIsland'
        else:
            to_id = NodeService.get_monkey_by_id(edge["to"])
            if to_id is None:
                to_label = NodeService.get_node_label(NodeService.get_node_by_id(edge["to"]))
            else:
                to_label = NodeService.get_monkey_label(to_id)

        RIGHT_ARROW = u"\u2192"
        return "%s %s %s" % (from_label, RIGHT_ARROW, to_label)



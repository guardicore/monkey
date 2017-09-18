from bson import ObjectId

from cc.database import mongo
import cc.services.node

__author__ = "itay.mizeretz"


class EdgeService:
    def __init__(self):
        pass

    @staticmethod
    def get_displayed_edge_by_id(edge_id):
        edge = mongo.db.edge.find({"_id": ObjectId(edge_id)})[0]
        return EdgeService.edge_to_displayed_edge(edge)

    @staticmethod
    def get_displayed_edges_by_to(to):
        edges = mongo.db.edge.find({"to": ObjectId(to)})
        new_edges = []
        # TODO: find better solution for this
        for i in range(edges.count()):
            new_edges.append(EdgeService.edge_to_displayed_edge(edges[i]))
        return new_edges

    @staticmethod
    def edge_to_displayed_edge(edge):
        services = {}
        os = {}
        exploits = []
        if len(edge["scans"]) > 0:
            services = EdgeService.services_to_displayed_services(edge["scans"][-1]["data"]["services"])
            os = edge["scans"][-1]["data"]["os"]

        for exploit in edge["exploits"]:
            new_exploit = EdgeService.exploit_to_displayed_exploit(exploit)

            if (len(exploits) > 0) and (exploits[-1]["exploiter"] == exploit["exploiter"]):
                exploit_container = exploits[-1]
            else:
                exploit_container =\
                    {
                        "exploiter": exploit["exploiter"],
                        "start_timestamp": exploit["timestamp"],
                        "end_timestamp": exploit["timestamp"],
                        "result": False,
                        "attempts": []
                    }

                exploits.append(exploit_container)

            exploit_container["attempts"].append(new_exploit)
            if new_exploit["result"]:
                exploit_container["result"] = True
            exploit_container["end_timestamp"] = new_exploit["timestamp"]

        displayed_edge = EdgeService.edge_to_net_edge(edge)
        displayed_edge["ip_address"] = edge["ip_address"]
        displayed_edge["services"] = services
        displayed_edge["os"] = os
        displayed_edge["exploits"] = exploits
        displayed_edge["_label"] = EdgeService.get_edge_label(displayed_edge)
        return displayed_edge

    @staticmethod
    def exploit_to_displayed_exploit(exploit):
        user = ""
        password = ""

        # TODO: The format that's used today to get the credentials is bad. Change it from monkey side and adapt.
        result = exploit["data"]["result"]
        if result:
            if "creds" in exploit["data"]["machine"]:
                user = exploit["data"]["machine"]["creds"].keys()[0]
                password = exploit["data"]["machine"]["creds"][user]
        else:
            if ("user" in exploit["data"]) and ("password" in exploit["data"]):
                user = exploit["data"]["user"]
                password = exploit["data"]["password"]

        return \
            {
                "timestamp": exploit["timestamp"],
                "user": user,
                "password": password,
                "result": result,
            }

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
        existing_ids = [x["_id"] for x in mongo.db.edge.find({"to": monkey["_id"]})]
        monkey_ids = [x["_id"] for x in mongo.db.monkey.find({})
                      if ("tunnel" not in x) and (x["_id"] not in existing_ids)]
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
    def services_to_displayed_services(services):
        # TODO: Consider returning extended information on services.
        return [x + ": " + services[x]["name"] for x in services]

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
        to_id = NodeService.get_monkey_by_id(edge["to"])
        if to_id is None:
            to_label = NodeService.get_node_label(NodeService.get_node_by_id(edge["to"]))
        else:
            to_label = NodeService.get_monkey_label(to_id)

        RIGHT_ARROW = u"\u2192"
        return "%s %s %s" % (from_label, RIGHT_ARROW, to_label)



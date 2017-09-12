from bson import ObjectId

from cc.database import mongo

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

        return \
            {
                "id": edge["_id"],
                "from": edge["from"],
                "to": edge["to"],
                "services": services,
                "os": os,
                "exploits": exploits
            }

    @staticmethod
    def exploit_to_displayed_exploit(exploit):
        user = ""
        password = ""

        # TODO: implement for other exploiters
        # TODO: The format that's used today to get the credentials is bad. Change it from monkey side and adapt.
        result = exploit["data"]["result"]
        if exploit["exploiter"] == "RdpExploiter":
            user = exploit["data"]["machine"]["creds"].keys()[0]
            password = exploit["data"]["machine"]["creds"][user]
        elif exploit["exploiter"] == "SmbExploiter":
            if result:
                user = exploit["data"]["machine"]["cred"].keys()[0]
                password = exploit["data"]["machine"]["cred"][user]
            else:
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
                "tunnel": False
            })
        return mongo.db.edge.find_one({"_id": edge_insert_result.inserted_id})

    @staticmethod
    def get_or_create_edge(edge_from, edge_to):
        tunnel_edge = mongo.db.edge.find_one({"from": edge_from, "to": edge_to})
        if tunnel_edge is None:
            tunnel_edge = EdgeService.insert_edge(edge_from, edge_to)

        return tunnel_edge

    @staticmethod
    def get_monkey_island_pseudo_edges():
        edges = []
        monkey_ids = [x["_id"] for x in mongo.db.monkey.find({}) if "tunnel" not in x]
        # We're using fake ids because the frontend graph module requires unique ids.
        # Collision with real id is improbable.
        count = 0
        for monkey_id in monkey_ids:
            count += 1
            edges.append(
                {
                    "id": ObjectId(hex(count)[2:].zfill(24)),
                    "from": monkey_id,
                    "to": ObjectId("000000000000000000000000")
                }
            )

        return edges

    @staticmethod
    def services_to_displayed_services(services):
        # TODO: Consider returning extended information on services.
        return [x + ": " + services[x]["name"] for x in services]

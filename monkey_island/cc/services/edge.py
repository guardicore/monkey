from bson import ObjectId

from cc.database import mongo

__author__ = "itay.mizeretz"


class EdgeService:
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
            services = edge["scans"][-1]["data"]["services"]
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
        result = False

        # TODO: implement for other exploiters

        if exploit["exploiter"] == "RdpExploiter":
            # TODO: check if there could be multiple creds
            result = exploit["data"]["result"]
            user = exploit["data"]["machine"]["creds"].keys()[0]
            password = exploit["data"]["machine"]["creds"][user]

        elif exploit["exploiter"] == "SmbExploiter":
            result = exploit["data"]["result"]
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
import flask_restful

from cc.database import mongo

__author__ = 'Barak'


class NetMap(flask_restful.Resource):
    def get(self, **kw):
        monkeys = [self.monkey_to_net_node(x) for x in mongo.db.monkey.find({})]
        nodes = [self.node_to_net_node(x) for x in mongo.db.node.find({})]
        edges = [self.edge_to_net_edge(x) for x in mongo.db.edge.find({})]

        return \
            {
                "nodes": monkeys + nodes,
                "edges": edges
            }

    def monkey_to_net_node(self, monkey):
        os = "unknown"
        if monkey["description"].lower().find("linux") != -1:
            os = "linux"
        elif monkey["description"].lower().find("windows") != -1:
            os = "windows"

        manual_run = (monkey["parent"][0][1] == None)
        return \
            {
                "id": monkey["_id"],
                "label": monkey["hostname"] + " : " + monkey["ip_addresses"][0],
                "group": ("manuallyInfected" if manual_run else "infected"),
                "os": os,
                "dead": monkey["dead"],
            }

    def node_to_net_node(self, node):
        os_version = "undefined"
        os_type = "undefined"
        found = False
        for edge in mongo.db.edge.find({"to": node["_id"]}):
            for scan in edge["scans"]:
                if scan["scanner"] != "TcpScanner":
                    continue
                os_type = scan["data"]["os"]["type"]
                if scan["data"]["os"].has_key("version"):
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

    def edge_to_net_edge(self, edge):
        return \
            {
                "id": edge["_id"],
                "from": edge["from"],
                "to": edge["to"]
            }

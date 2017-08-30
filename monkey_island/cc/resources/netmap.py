import flask_restful

from cc.services.node import NodeService
from cc.database import mongo

__author__ = 'Barak'


class NetMap(flask_restful.Resource):
    def get(self, **kw):
        monkeys = [NodeService.monkey_to_net_node(x) for x in mongo.db.monkey.find({})]
        nodes = [NodeService.node_to_net_node(x) for x in mongo.db.node.find({})]
        edges = [self.edge_to_net_edge(x) for x in mongo.db.edge.find({})]

        return \
            {
                "nodes": monkeys + nodes,
                "edges": edges
            }

    def edge_to_net_edge(self, edge):
        return \
            {
                "id": edge["_id"],
                "from": edge["from"],
                "to": edge["to"]
            }

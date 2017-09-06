import flask_restful

from cc.services.edge import EdgeService
from cc.services.node import NodeService
from cc.database import mongo

__author__ = 'Barak'


class NetMap(flask_restful.Resource):
    def get(self, **kw):
        monkeys = [NodeService.monkey_to_net_node(x) for x in mongo.db.monkey.find({})]
        nodes = [NodeService.node_to_net_node(x) for x in mongo.db.node.find({})]
        edges = [self.edge_to_net_edge(x) for x in mongo.db.edge.find({})]
        monkey_island = []
        if NodeService.get_monkey_island_monkey() is None:
            monkey_island = [NodeService.get_monkey_island_pseudo_net_node()]
            # TODO: implement when monkey exists on island
            edges += EdgeService.get_monkey_island_pseudo_edges()

        return \
            {
                "nodes": monkeys + nodes + monkey_island,
                "edges": edges
            }

    def edge_to_net_edge(self, edge):
        return \
            {
                "id": edge["_id"],
                "from": edge["from"],
                "to": edge["to"]
            }

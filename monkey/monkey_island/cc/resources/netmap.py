import flask_restful

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.netmap.net_edge import NetEdgeService
from monkey_island.cc.services.netmap.net_node import NetNodeService

__author__ = 'Barak'


class NetMap(flask_restful.Resource):
    @jwt_required
    def get(self, **kw):
        net_nodes = NetNodeService.get_all_net_nodes()
        net_edges = NetEdgeService.get_all_net_edges()

        return \
            {
                "nodes": net_nodes,
                "edges": net_edges
            }

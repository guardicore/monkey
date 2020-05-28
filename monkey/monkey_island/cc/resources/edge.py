import flask_restful
from flask import request

from monkey_island.cc.services.edge.displayed_edge import DisplayedEdgeService

__author__ = 'Barak'


class Edge(flask_restful.Resource):
    def get(self):
        edge_id = request.args.get('id')
        displayed_edge = DisplayedEdgeService.get_displayed_edge_by_id(edge_id)
        if edge_id:
            return {"edge": displayed_edge}

        return {}

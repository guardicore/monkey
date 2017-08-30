from bson import ObjectId
from flask import request
import flask_restful

from cc.database import mongo
from cc.services.edge import EdgeService

__author__ = 'Barak'


class Edge(flask_restful.Resource):
    def get(self):
        edge_id = request.args.get('id')

        if edge_id:
            return {"edge": EdgeService.get_displayed_edge_by_id(edge_id)}

        return {}

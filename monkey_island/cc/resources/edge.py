from bson import ObjectId
from flask import request
import flask_restful

from cc.database import mongo

__author__ = 'Barak'


class Edge(flask_restful.Resource):
    def get(self):
        id = request.args.get('id')
        to = request.args.get('to')
        if id:
            edge = mongo.db.edge.find({"_id": ObjectId(id)})[0]
            return {"edge": edge}
        if to:
            edges = mongo.db.edge.find({"to": ObjectId(to)})
            new_edges = []
            # TODO: find better solution for this
            for i in range(edges.count()):
                new_edges.append(edges[i])
            return {"edges": new_edges}
        return {}

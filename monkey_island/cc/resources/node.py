from bson import ObjectId
from flask import request
import flask_restful

from cc.database import mongo
from cc.services.edge import EdgeService
from cc.services.node import NodeService

__author__ = 'Barak'


class Node(flask_restful.Resource):
    def get(self):
        node_id = request.args.get('id')
        if node_id:
            return NodeService.get_displayed_node_by_id(request.args.get('node_id'))

        return {}

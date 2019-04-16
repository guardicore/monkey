from flask import request
import flask_restful

from monkey_island.cc.auth import jwt_required
from monkey_island.cc.services.node import NodeService

__author__ = 'Barak'


class Node(flask_restful.Resource):
    @jwt_required()
    def get(self):
        node_id = request.args.get('id')
        if node_id:
            return NodeService.get_displayed_node_by_id(node_id)

        return {}

import flask_restful
from flask import request

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.node import NodeService

__author__ = 'Barak'


class Node(flask_restful.Resource):
    @jwt_required
    def get(self):
        node_id = request.args.get('id')
        if node_id:
            return NodeService.get_displayed_node_by_id(node_id)

        return {}

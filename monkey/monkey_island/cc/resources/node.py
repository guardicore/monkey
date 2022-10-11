from flask import request

from monkey_island.cc.repository import INodeRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.node import NodeService


class Node(AbstractResource):
    urls = ["/api/netmap/node"]

    def __init__(self, node_repository: INodeRepository):
        self.node_repository = node_repository

    @jwt_required
    def get(self):
        node_id = request.args.get("id")
        if node_id:
            return NodeService.get_displayed_node_by_id(node_id)
        else:
            return list(self.node_repository.get_nodes())

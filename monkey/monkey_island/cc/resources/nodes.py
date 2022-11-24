from http import HTTPStatus

from monkey_island.cc.repositories import INodeRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource


class Nodes(AbstractResource):
    urls = ["/api/nodes"]

    def __init__(self, node_repository: INodeRepository):
        self._node_repository = node_repository

    def get(self):
        return self._node_repository.get_nodes(), HTTPStatus.OK

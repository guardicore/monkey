from http import HTTPStatus

from flask_security import auth_token_required

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import INodeRepository


class Nodes(AbstractResource):
    urls = ["/api/nodes"]

    def __init__(self, node_repository: INodeRepository):
        self._node_repository = node_repository

    @auth_token_required
    def get(self):
        return self._node_repository.get_nodes(), HTTPStatus.OK

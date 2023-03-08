from http import HTTPStatus

from flask_security import auth_token_required, roles_required

from common import AccountRoles
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import IMachineRepository


class Machines(AbstractResource):
    urls = ["/api/machines"]

    def __init__(self, machine_repository: IMachineRepository):
        self._machine_repository = machine_repository

    @auth_token_required
    @roles_required(AccountRoles.ISLAND.name)
    def get(self):
        return self._machine_repository.get_machines(), HTTPStatus.OK

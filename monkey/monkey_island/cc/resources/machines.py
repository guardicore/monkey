from http import HTTPStatus

from flask_security import auth_token_required

from monkey_island.cc.repositories import IMachineRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource


class Machines(AbstractResource):
    urls = ["/api/machines"]

    def __init__(self, machine_repository: IMachineRepository):
        self._machine_repository = machine_repository

    @auth_token_required
    def get(self):
        return self._machine_repository.get_machines(), HTTPStatus.OK

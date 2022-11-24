from http import HTTPStatus

from monkey_island.cc.repositories import IMachineRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class Machines(AbstractResource):
    urls = ["/api/machines"]

    def __init__(self, machine_repository: IMachineRepository):
        self._machine_repository = machine_repository

    @jwt_required
    def get(self):
        return self._machine_repository.get_machines(), HTTPStatus.OK

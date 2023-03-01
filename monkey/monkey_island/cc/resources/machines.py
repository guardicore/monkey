from http import HTTPStatus

from monkey_island.cc.repositories import IMachineRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource


class Machines(AbstractResource):
    urls = ["/api/machines"]

    def __init__(self, machine_repository: IMachineRepository):
        self._machine_repository = machine_repository

    def get(self):
        return self._machine_repository.get_machines(), HTTPStatus.OK

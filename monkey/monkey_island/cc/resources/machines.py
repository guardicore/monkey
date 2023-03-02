from http import HTTPStatus

from monkey_island.cc.flask_utils import AbstractResource, jwt_required
from monkey_island.cc.repositories import IMachineRepository


class Machines(AbstractResource):
    urls = ["/api/machines"]

    def __init__(self, machine_repository: IMachineRepository):
        self._machine_repository = machine_repository

    @jwt_required
    def get(self):
        return self._machine_repository.get_machines(), HTTPStatus.OK

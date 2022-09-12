from http import HTTPStatus

from flask import make_response

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services import RepositoryService


class ClearSimulationData(AbstractResource):
    urls = ["/api/clear-simulation-data"]

    def __init__(self, repository_service: RepositoryService):
        self._repository_service = repository_service

    @jwt_required
    def post(self):
        """
        Clear all data collected during the simulation
        """

        self._repository_service.clear_simulation_data()
        return make_response({}, HTTPStatus.NO_CONTENT)

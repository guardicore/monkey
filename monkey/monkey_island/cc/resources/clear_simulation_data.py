from flask import make_response

from monkey_island.cc.repository import RemovalError
from monkey_island.cc.repository.i_credentials_repository import ICredentialsRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.database import Database


class ClearSimulationData(AbstractResource):
    urls = ["/api/clear-simulation-data"]

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    @jwt_required
    def post(self):
        """
        Clear all data collected during the simulation
        """
        Database.reset_db(reset_config=False)
        self._credentials_repository.remove_stolen_credentials()

        return make_response({}, 200)

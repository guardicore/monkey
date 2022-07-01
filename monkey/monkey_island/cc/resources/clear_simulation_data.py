from flask import make_response

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.database import Database


class ClearSimulationData(AbstractResource):
    urls = ["/api/clear-simulation-data"]

    @jwt_required
    def post(self):
        """
        Clear all data collected during the simulation
        """
        Database.reset_db(reset_config=False)

        return make_response({}, 200)

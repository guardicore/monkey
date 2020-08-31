import json

import flask_restful
from flask import make_response, request

from monkey_island.cc.services.config import ConfigService


class StartedOnIsland(flask_restful.Resource):

    # Used by monkey. can't secure.
    def post(self):
        data = json.loads(request.data)
        if data['started_on_island']:
            ConfigService.set_started_on_island(True)
        return make_response({}, 200)

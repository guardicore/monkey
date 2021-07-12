import json

import flask_restful
from flask import make_response, request

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.mode import island_mode_service
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum


class IslandMode(flask_restful.Resource):
    @jwt_required
    def post(self):
        body = json.loads(request.data)
        mode_str = body.get("mode")
        mode = IslandModeEnum(mode_str)
        island_mode_service.set_mode(mode)

        # TODO return status
        return make_response({})

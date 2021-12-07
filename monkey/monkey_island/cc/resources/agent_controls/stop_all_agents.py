import json

import flask_restful
from flask import make_response, request

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.resources.utils.semaphores import AGENT_KILLING_SEMAPHORE
from monkey_island.cc.services.infection_lifecycle import set_stop_all, was_monkey_killed


class StopAllAgents(flask_restful.Resource):
    @jwt_required
    def post(self):
        with AGENT_KILLING_SEMAPHORE:
            data = json.loads(request.data)
            if data["kill_time"]:
                set_stop_all(data["kill_time"])
                return make_response({}, 200)
            else:
                return make_response({}, 400)

    def get(self, monkey_guid):
        return {"stop_agent": was_monkey_killed(monkey_guid)}

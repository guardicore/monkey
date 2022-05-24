import json

from flask import make_response, request

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.resources.utils.semaphores import agent_killing_mutex
from monkey_island.cc.services.infection_lifecycle import set_stop_all, should_agent_die


class StopAllAgents(AbstractResource):
    # API Spec: This is an action and there's no "resource"; RPC-style endpoint?
    urls = ["/api/monkey-control/stop-all-agents"]

    @jwt_required
    def post(self):
        with agent_killing_mutex:
            data = json.loads(request.data)
            if data["kill_time"]:
                set_stop_all(data["kill_time"])
                return make_response({}, 200)
            else:
                return make_response({}, 400)

    # API Spec: This is the exact same thing as what's in StopAgentCheck
    def get(self, monkey_guid):
        return {"stop_agent": should_agent_die(monkey_guid)}

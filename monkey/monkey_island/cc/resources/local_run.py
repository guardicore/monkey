import json

import flask_restful
from flask import jsonify, make_response, request

from monkey_island.cc.models import Monkey
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService


class LocalRun(flask_restful.Resource):
    @jwt_required
    def get(self):
        island_monkey = NodeService.get_monkey_island_monkey()
        if island_monkey is not None:
            is_monkey_running = not Monkey.get_single_monkey_by_id(island_monkey["_id"]).is_dead()
        else:
            is_monkey_running = False

        return jsonify(is_running=is_monkey_running)

    @jwt_required
    def post(self):
        body = json.loads(request.data)
        if body.get("action") == "run":
            local_run = LocalMonkeyRunService.run_local_monkey()
            return jsonify(is_running=local_run[0], error_text=local_run[1])

        # default action
        return make_response({"error": "Invalid action"}, 500)

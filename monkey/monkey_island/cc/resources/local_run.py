import json

from flask import jsonify, make_response, request
from flask_security import auth_token_required, roles_required

from common import AccountRole
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService


class LocalRun(AbstractResource):
    urls = ["/api/local-monkey"]

    def __init__(self, local_monkey_run_service: LocalMonkeyRunService):
        self._local_monkey_run_service = local_monkey_run_service

    # API Spec: This should be an RPC-style endpoint
    @auth_token_required
    @roles_required(AccountRole.ISLAND_INTERFACE.name)
    def post(self):
        body = json.loads(request.data)
        if body.get("action") == "run":
            local_run = self._local_monkey_run_service.run_local_monkey()
            # API Spec: Feels weird to return "error_text" even when "is_running" is True
            return jsonify(is_running=local_run[0], error_text=local_run[1])

        # default action
        # API Spec: Why is this 500? 500 should be returned in case an exception occurs on the
        # server. 40x makes more sense.
        return make_response({"error": "Invalid action"}, 500)

import json

from flask import jsonify, make_response, request
from flask_security import auth_token_required, roles_accepted

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole
from monkey_island.cc.services.authentication_service.i_otp_generator import IOTPGenerator
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService


class LocalRun(AbstractResource):
    urls = ["/api/local-monkey"]

    def __init__(
        self, local_monkey_run_service: LocalMonkeyRunService, otp_generator: IOTPGenerator
    ):
        self._local_monkey_run_service = local_monkey_run_service
        self._otp_generator = otp_generator

    # API Spec: This should be an RPC-style endpoint
    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def post(self):
        body = json.loads(request.data)
        if body.get("action") == "run":
            otp = self._otp_generator.generate_otp()
            local_run = self._local_monkey_run_service.run_local_monkey(otp)
            # API Spec: Feels weird to return "error_text" even when "is_running" is True
            return jsonify(is_running=local_run[0], error_text=local_run[1])

        # default action
        # API Spec: Why is this 500? 500 should be returned in case an exception occurs on the
        # server. 40x makes more sense.
        return make_response({"error": "Invalid action"}, 500)

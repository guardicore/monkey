import logging

import flask_restful
from flask import make_response, request

import monkey_island.cc.environment.environment_singleton as env_singleton
from common.utils.exceptions import InvalidRegistrationCredentialsError, RegistrationNotNeededError
from monkey_island.cc.resources.auth.credential_utils import get_username_password_from_request
from monkey_island.cc.services.authentication import AuthenticationService

logger = logging.getLogger(__name__)


class Registration(flask_restful.Resource):
    def get(self):
        is_registration_needed = env_singleton.env.needs_registration()
        return {"needs_registration": is_registration_needed}

    def post(self):
        username, password = get_username_password_from_request(request)

        try:
            AuthenticationService.register_new_user(username, password)
            return make_response({"error": ""}, 200)
        except (InvalidRegistrationCredentialsError, RegistrationNotNeededError) as e:
            return make_response({"error": str(e)}, 400)

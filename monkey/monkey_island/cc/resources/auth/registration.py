import logging

import flask_restful
from flask import make_response, request

import monkey_island.cc.environment.environment_singleton as env_singleton
from common.utils.exceptions import InvalidRegistrationCredentialsError, RegistrationNotNeededError
from monkey_island.cc.resources.auth.credential_utils import (
    get_user_credentials_from_request,
    get_username_password_from_request,
)
from monkey_island.cc.services.authentication import AuthenticationService
from monkey_island.cc.setup.mongo.database_initializer import reset_database

logger = logging.getLogger(__name__)


class Registration(flask_restful.Resource):
    def get(self):
        is_registration_needed = env_singleton.env.needs_registration()
        return {"needs_registration": is_registration_needed}

    def post(self):
        credentials = get_user_credentials_from_request(request)

        try:
            env_singleton.env.try_add_user(credentials)
            username, password = get_username_password_from_request(request)
            AuthenticationService.reset_datastore_encryptor(username, password)
            reset_database()
            return make_response({"error": ""}, 200)
        except (InvalidRegistrationCredentialsError, RegistrationNotNeededError) as e:
            return make_response({"error": str(e)}, 400)

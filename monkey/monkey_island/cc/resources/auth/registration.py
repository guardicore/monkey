import json
import logging

import flask_restful
from flask import make_response, request

import monkey_island.cc.environment.environment_singleton as env_singleton
import monkey_island.cc.resources.auth.password_utils as password_utils
from common.utils.exceptions import InvalidRegistrationCredentialsError, RegistrationNotNeededError
from monkey_island.cc.environment.user_creds import UserCreds
from monkey_island.cc.setup.mongo.database_initializer import reset_database

logger = logging.getLogger(__name__)


class Registration(flask_restful.Resource):
    def get(self):
        is_registration_needed = env_singleton.env.needs_registration()
        return {"needs_registration": is_registration_needed}

    def post(self):
        credentials = _get_user_credentials_from_request(request)

        try:
            env_singleton.env.try_add_user(credentials)
            reset_database()
            return make_response({"error": ""}, 200)
        except (InvalidRegistrationCredentialsError, RegistrationNotNeededError) as e:
            return make_response({"error": str(e)}, 400)


def _get_user_credentials_from_request(request):
    cred_dict = json.loads(request.data)

    username = cred_dict.get("user", "")
    password = cred_dict.get("password", "")
    password_hash = password_utils.hash_password(password)

    return UserCreds(username, password_hash)

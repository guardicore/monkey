import json

import bcrypt
import flask_restful
from flask import make_response, request

import monkey_island.cc.environment.environment_singleton as env_singleton
from common.utils.exceptions import InvalidRegistrationCredentialsError, RegistrationNotNeededError
from monkey_island.cc.environment.user_creds import UserCreds


class Registration(flask_restful.Resource):
    def get(self):
        return {"needs_registration": env_singleton.env.needs_registration()}

    def post(self):
        credentials = _get_user_credentials_from_request(request)

        try:
            env_singleton.env.try_add_user(credentials)
            return make_response({"error": ""}, 200)
        except (InvalidRegistrationCredentialsError, RegistrationNotNeededError) as e:
            return make_response({"error": str(e)}, 400)


def _get_user_credentials_from_request(request):
    cred_dict = json.loads(request.data)

    username = cred_dict.get("user", "")
    password = cred_dict.get("password", "")
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

    return UserCreds(username, password_hash)

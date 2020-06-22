import flask_restful
from flask import request, make_response

from common.utils.exceptions import InvalidRegistrationCredentialsError, RegistrationNotNeededError
import monkey_island.cc.environment.environment_singleton as env_singleton
from monkey_island.cc.environment.user_creds import UserCreds


class Registration(flask_restful.Resource):
    def get(self):
        return {'needs_registration': env_singleton.env.needs_registration()}

    def post(self):
        credentials = UserCreds.get_from_json(request.data)
        try:
            env_singleton.env.try_add_user(credentials)
            return make_response({"error": ""}, 200)
        except (InvalidRegistrationCredentialsError, RegistrationNotNeededError) as e:
            return make_response({"error": str(e)}, 400)


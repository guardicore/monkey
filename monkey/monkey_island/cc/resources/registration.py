import flask_restful
from flask import request, make_response

from common.utils.exceptions import InvalidRegistrationCredentials
from monkey_island.cc.environment.environment_singleton import env
from monkey_island.cc.environment.user_creds import UserCreds


class Registration(flask_restful.Resource):
    def get(self):
        return {'needs_registration': env.needs_registration()}

    def post(self):
        credentials = UserCreds.get_from_json(request.data)
        try:
            env.try_add_user(credentials)
            return make_response({"error": ""}, 300)
        except InvalidRegistrationCredentials as e:
            return make_response({"error": e}, 400)


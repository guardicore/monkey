import logging

import flask_restful
from flask import make_response, request

import monkey_island.cc.environment.environment_singleton as env_singleton
from common.utils.exceptions import InvalidRegistrationCredentialsError, RegistrationNotNeededError
from monkey_island.cc.resources.auth.credential_utils import (
    get_secret_from_request,
    get_user_credentials_from_request,
)
from monkey_island.cc.server_utils.encryption import remove_old_datastore_key, setup_datastore_key
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
            remove_old_datastore_key()
            setup_datastore_key(get_secret_from_request(request))
            reset_database()
            return make_response({"error": ""}, 200)
        except (InvalidRegistrationCredentialsError, RegistrationNotNeededError) as e:
            return make_response({"error": str(e)}, 400)

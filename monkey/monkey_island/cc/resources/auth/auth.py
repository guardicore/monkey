import json
import logging
from functools import wraps

import flask_jwt_extended
import flask_restful
from flask import make_response, request
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt import PyJWTError
from werkzeug.security import safe_str_cmp

import monkey_island.cc.environment.environment_singleton as env_singleton
import monkey_island.cc.resources.auth.user_store as user_store

logger = logging.getLogger(__name__)


def init_jwt(app):
    user_store.UserStore.set_users(env_singleton.env.get_auth_users())
    _ = flask_jwt_extended.JWTManager(app)
    logger.debug("Initialized JWT with secret key that started with " + app.config["JWT_SECRET_KEY"][:4])


class Authenticate(flask_restful.Resource):
    """
    Resource for user authentication. The user provides the username and hashed password and we give them a JWT.
    See `AuthService.js` file for the frontend counterpart for this code.
    """
    @staticmethod
    def _authenticate(username, secret):
        user = user_store.UserStore.username_table.get(username, None)
        if user and safe_str_cmp(user.secret.encode('utf-8'), secret.encode('utf-8')):
            return user

    def post(self):
        """
        Example request:
        {
            "username": "my_user",
            "password": "343bb87e553b05430e5c44baf99569d4b66..."
        }
        """
        credentials = json.loads(request.data)
        # Unpack auth info from request
        username = credentials["username"]
        secret = credentials["password"]
        # If the user and password have been previously registered
        if self._authenticate(username, secret):
            access_token = flask_jwt_extended.create_access_token(identity=user_store.UserStore.username_table[username].id)
            logger.debug(f"Created access token for user {username} that begins with {access_token[:4]}")
            return make_response({"access_token": access_token, "error": ""}, 200)
        else:
            return make_response({"error": "Invalid credentials"}, 401)


# See https://flask-jwt-extended.readthedocs.io/en/stable/custom_decorators/
def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            flask_jwt_extended.verify_jwt_in_request()
            return fn(*args, **kwargs)
        # Catch authentication related errors in the verification or inside the called function. All other exceptions propagate
        except (JWTExtendedException, PyJWTError) as e:
            return make_response({"error": f"Authentication error: {str(e)}"}, 401)

    return wrapper

import logging
from functools import wraps

import flask_jwt_extended
from flask import make_response
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt import PyJWTError

logger = logging.getLogger(__name__)


def create_access_token(username):
    access_token = flask_jwt_extended.create_access_token(identity=username)
    logger.debug(f"Created access token for user {username} that begins with {access_token[:4]}")

    return access_token


# See https://flask-jwt-extended.readthedocs.io/en/stable/custom_decorators/
def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            flask_jwt_extended.verify_jwt_in_request()
            return fn(*args, **kwargs)
        # Catch authentication related errors in the verification or inside the called function.
        # All other exceptions propagate
        except (JWTExtendedException, PyJWTError) as e:
            return make_response({"error": f"Authentication error: {str(e)}"}, 401)

    return wrapper

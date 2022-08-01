import logging
from http import HTTPStatus

import flask_jwt_extended
from flask import make_response, request

from common.utils.exceptions import IncorrectCredentialsError
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.auth.credential_utils import get_username_password_from_request
from monkey_island.cc.resources.request_authentication import create_access_token
from monkey_island.cc.services import AuthenticationService

logger = logging.getLogger(__name__)


def init_jwt(app):
    _ = flask_jwt_extended.JWTManager(app)
    logger.debug(
        "Initialized JWT with secret key that started with " + app.config["JWT_SECRET_KEY"][:4]
    )


class Authenticate(AbstractResource):
    """
    Resource for user authentication. The user provides the username and password and we \
    give them a JWT. \
    See `AuthService.js` file for the frontend counterpart for this code. \

    """

    urls = ["/api/authenticate"]

    def __init__(self, authentication_service: AuthenticationService):
        self._authentication_service = authentication_service

    def post(self):
        """
        Example request: \
        { \
            "username": "my_user", \
            "password": "my_password" \
        } \

        """
        username, password = get_username_password_from_request(request)

        try:
            self._authentication_service.authenticate(username, password)
            access_token = create_access_token(username)
        except IncorrectCredentialsError:
            return make_response({"error": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED)

        # API Spec: Why are we sending "error" here?
        return make_response({"access_token": access_token, "error": ""}, HTTPStatus.OK)

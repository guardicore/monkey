import logging
from http import HTTPStatus

import flask_jwt_extended
from flask import make_response, request

from common.utils.exceptions import IncorrectCredentialsError
from monkey_island.cc.flask_utils import AbstractResource
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
    A resource for user authentication
    """

    urls = ["/api/authenticate"]

    def __init__(self, authentication_service: AuthenticationService):
        self._authentication_service = authentication_service

    def post(self):
        """
        Authenticates a user

        Gets a username and password from the request sent from the client, authenticates, and
        returns an access token

        :return: Access token in the response body
        :raises IncorrectCredentialsError: If credentials are invalid
        """

        username, password = get_username_password_from_request(request)

        try:
            self._authentication_service.authenticate(username, password)
            access_token = create_access_token(username)
        except IncorrectCredentialsError:
            return make_response({"error": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED)

        return make_response({"access_token": access_token}, HTTPStatus.OK)

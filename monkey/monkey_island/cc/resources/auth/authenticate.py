import logging
from http import HTTPStatus

from flask import jsonify, make_response, request
from flask_login import current_user, login_required, login_user

from common.utils.exceptions import IncorrectCredentialsError
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.resources.auth.credential_utils import get_username_password_from_request
from monkey_island.cc.services import AuthenticationService

logger = logging.getLogger(__name__)


class Authenticate(AbstractResource):
    """
    A resource for user authentication
    """

    urls = ["/api/authenticate"]

    def __init__(self, authentication_service: AuthenticationService):
        self._authentication_service = authentication_service

    def get(self):
        return jsonify({"authenticated": current_user.is_authenticated})

    @login_required
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
            user = self._authentication_service.authenticate(username, password)
        except IncorrectCredentialsError:
            return make_response({"error": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED)

        login_user(user)
        return jsonify({"login": True})

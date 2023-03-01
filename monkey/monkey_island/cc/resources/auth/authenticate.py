import logging
from http import HTTPStatus

from flask import jsonify, make_response, request
from flask_security import current_user
from flask_security.views import login
from flask.typing import ResponseValue

from monkey_island.cc.resources.AbstractResource import AbstractResource
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

    # TODO: Added for debugging. Remove before closing #2157.
    def get(self):
        return jsonify({"authenticated": current_user.is_authenticated})

    def post(self):
        """
        Authenticates a user

        Gets a username and password from the request sent from the client, authenticates, and
        returns an access token

        :return: Access token in the response body
        :raises IncorrectCredentialsError: If credentials are invalid
        """

        response: ResponseValue = login()
        if response.status_code == HTTPStatus.OK:
            username, password = get_username_password_from_request(request)
            self._authentication_service.unlock_repository_encryptor(username, password)

        return make_response(response)

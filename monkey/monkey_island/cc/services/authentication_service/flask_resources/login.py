import logging
from http import HTTPStatus

from flask import Response, make_response, request
from flask.typing import ResponseValue
from flask_security.views import login

from monkey_island.cc.flask_utils import AbstractResource, responses

from ..authentication_facade import AuthenticationFacade
from .utils import get_username_password_from_request, include_auth_token

logger = logging.getLogger(__name__)


class Login(AbstractResource):
    """
    A resource for user authentication
    """

    urls = ["/api/login"]

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    # Can't be secured, used for login
    @include_auth_token
    def post(self):
        """
        Authenticates a user

        Gets a username and password from the request sent from the client, authenticates, and
        returns an access token

        :return: Access token in the response body
        """
        try:
            username, password = get_username_password_from_request(request)
        except Exception:
            return responses.make_response_to_invalid_request()

        response: ResponseValue = login()

        if not isinstance(response, Response):
            return responses.make_response_to_invalid_request()

        if response.status_code == HTTPStatus.OK:
            self._authentication_facade.handle_successful_login(username, password)

        return make_response(response)

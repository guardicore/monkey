import logging
from http import HTTPStatus

from flask import Response, make_response
from flask.typing import ResponseValue
from flask_security.views import logout

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.server_utils.response_utils import response_to_invalid_request
from monkey_island.cc.services import AuthenticationService

logger = logging.getLogger(__name__)


class Logout(AbstractResource):
    """
    A resource logging out an authenticated user
    """

    urls = ["/api/logout"]

    def __init__(self, authentication_service: AuthenticationService):
        self._authentication_service = authentication_service

    def post(self):
        try:
            response: ResponseValue = logout()
        except Exception:
            return response_to_invalid_request()

        if not isinstance(response, Response):
            return response_to_invalid_request()
        if response.status_code == HTTPStatus.OK:
            self._authentication_service.lock_repository_encryptor()

        return make_response(response)

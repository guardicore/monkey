import logging
from http import HTTPStatus

from flask import make_response
from flask.typing import ResponseValue
from flask_security.views import logout

from monkey_island.cc.resources.AbstractResource import AbstractResource
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
        response: ResponseValue = logout()
        if response.status_code == HTTPStatus.OK:
            self._authentication_service.lock_repository_encryptor()

        return make_response(response)

import logging
from http import HTTPStatus

from flask import Response, make_response
from flask.typing import ResponseValue
from flask_security.views import logout

from monkey_island.cc.flask_utils import AbstractResource, responses

from ..authentication_facade import AuthenticationFacade

logger = logging.getLogger(__name__)


class Logout(AbstractResource):
    """
    A resource logging out an authenticated user
    """

    urls = ["/api/logout"]

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    def post(self):
        try:
            response: ResponseValue = logout()
        except Exception:
            return responses.make_response_to_invalid_request()

        if not isinstance(response, Response):
            return responses.make_response_to_invalid_request()
        if response.status_code == HTTPStatus.OK:
            self._authentication_facade.handle_successful_logout()

        return make_response(response)

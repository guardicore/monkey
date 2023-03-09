import logging
from http import HTTPStatus

from flask import Response, make_response, request
from flask.typing import ResponseValue
from flask_security.views import register

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.server_utils.response_utils import response_to_invalid_request
from monkey_island.cc.services.authentication_service import AuthenticationService
from monkey_island.cc.services.authentication_service.utils import (
    get_username_password_from_request,
)

logger = logging.getLogger(__name__)


class Register(AbstractResource):
    """
    A resource for user registration
    """

    urls = ["/api/register"]

    def __init__(self, authentication_service: AuthenticationService):
        self._authentication_service = authentication_service

    def post(self):
        """
        Registers a new user using flask security register

        """
        try:
            username, password = get_username_password_from_request(request)
            response: ResponseValue = register()
        except Exception:
            return response_to_invalid_request()

        # Register view treat the request as form submit which may return something
        # that it is not a response
        if not isinstance(response, Response):
            return response_to_invalid_request()

        if response.status_code == HTTPStatus.OK:
            self._authentication_service.handle_successful_registration(username, password)

        return make_response(response)

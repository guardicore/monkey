import logging
from http import HTTPStatus

from flask import Response, make_response, request
from flask.typing import ResponseValue
from flask_login import current_user
from flask_security.views import register

from monkey_island.cc.flask_utils import AbstractResource, responses

from ..authentication_facade import AuthenticationFacade
from .utils import get_username_password_from_request, include_auth_token

logger = logging.getLogger(__name__)


class Register(AbstractResource):
    """
    A resource for user registration
    """

    urls = ["/api/register"]

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    @include_auth_token
    def post(self):
        """
        Registers a new user using flask security register

        """
        try:
            if not self._authentication_facade.needs_registration():
                return {
                    "errors": ["A user already exists. Only a single user can be registered."]
                }, HTTPStatus.CONFLICT
            username, password = get_username_password_from_request(request)
            response: ResponseValue = register()
            # TODO send these back
            _tokens = self._authentication_facade.generate_user_tokens(current_user)
            del _tokens
        except Exception:
            return responses.make_response_to_invalid_request()

        # Register view treat the request as form submit which may return something
        # that it is not a response
        if not isinstance(response, Response):
            return responses.make_response_to_invalid_request()

        if response.status_code == HTTPStatus.OK:
            self._authentication_facade.handle_successful_registration(username, password)

        return make_response(response)

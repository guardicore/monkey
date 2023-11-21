import logging
from http import HTTPStatus
from typing import List

from flask import Response, current_app, make_response, request
from flask.typing import ResponseValue
from flask_security.views import register

from monkey_island.cc.flask_utils import AbstractResource, responses

from ..authentication_facade import AuthenticationFacade
from .utils import add_token_ttl_to_response, get_username_password_from_request, include_auth_token

logger = logging.getLogger(__name__)


class Register(AbstractResource):
    """
    A resource for user registration
    """

    urls = ["/api/register"]

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    # Can't be secured, used for registration
    @include_auth_token
    def post(self):
        """
        Registers a new user using flask security register

        """
        if not self._authentication_facade.needs_registration():
            return {
                "errors": ["A user already exists. Only a single user can be registered."]
            }, HTTPStatus.CONFLICT

        try:
            username, password = get_username_password_from_request(request)
        except Exception:
            return responses.make_response_to_invalid_request()

        errors = self._validate_username_and_password(username, password)
        if errors:
            return make_response({"response": {"errors": errors}}, HTTPStatus.BAD_REQUEST)

        response: ResponseValue = register()

        # Register view treat the request as form submit which may return something
        # that it is not a response
        if not isinstance(response, Response):
            return responses.make_response_to_invalid_request()

        if response.status_code == HTTPStatus.OK:
            self._authentication_facade.handle_successful_registration(username, password)
            response = add_token_ttl_to_response(
                response, self._authentication_facade.token_ttl_sec
            )

        return make_response(response)

    def _validate_username_and_password(self, username: str, password: str) -> List[str]:
        validation_messages = []
        security = current_app.extensions["security"]
        username_util = security._username_util
        password_util = security._password_util

        username_errors = username_util.validate(username)[0]
        password_errors = password_util.validate(password, False)[0]
        if username_errors is not None:
            validation_messages.append(username_errors)
        elif username == "":
            validation_messages.append("Username not provided")

        if password_errors is not None:
            validation_messages += password_errors

        return validation_messages

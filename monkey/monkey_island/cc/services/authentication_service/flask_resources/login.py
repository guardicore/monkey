import logging
from http import HTTPStatus
from threading import Lock

from flask import Response, make_response, request
from flask.typing import ResponseValue
from flask_limiter import Limiter, RateLimitExceeded
from flask_security.views import login

from monkey_island.cc.flask_utils import AbstractResource, responses

from ..authentication_facade import AuthenticationFacade
from .utils import add_token_ttl_to_response, get_username_password_from_request, include_auth_token

logger = logging.getLogger(__name__)

MAX_LOGIN_REQUESTS_PER_SECOND = 5


class Login(AbstractResource):
    """
    A resource for user authentication
    """

    urls = ["/api/login"]
    lock = Lock()
    limiter = None

    def __init__(self, authentication_facade: AuthenticationFacade, limiter: Limiter):
        self._authentication_facade = authentication_facade
        with Login.lock:
            if Login.limiter is None:
                Login.limiter = limiter.limit(
                    f"{MAX_LOGIN_REQUESTS_PER_SECOND}/second",
                    key_func=lambda: "key",  # Limit all requests, not just per IP
                    per_method=True,
                )

    # Can't be secured, used for login
    @include_auth_token
    def post(self):
        """
        Authenticates a user

        Gets a username and password from the request sent from the client, authenticates, and
        returns an access token

        :return: Access token in the response body
        """
        if Login.limiter is None:
            raise RuntimeError("limiter has not been initialized")

        try:
            with Login.limiter:
                return self._handle_login_request()
        except RateLimitExceeded:
            return make_response("Rate limit exceeded", HTTPStatus.TOO_MANY_REQUESTS)

    def _handle_login_request(self):
        try:
            username, password = get_username_password_from_request(request)
        except Exception:
            return responses.make_response_to_invalid_request()

        response: ResponseValue = login()

        if not isinstance(response, Response):
            return responses.make_response_to_invalid_request()

        if response.status_code == HTTPStatus.OK:
            self._authentication_facade.handle_successful_login(username, password)
            response = add_token_ttl_to_response(
                response, self._authentication_facade.token_ttl_sec
            )

        return make_response(response)

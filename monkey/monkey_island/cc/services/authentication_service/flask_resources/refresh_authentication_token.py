import logging
from http import HTTPStatus
from threading import Lock

from flask import make_response
from flask_limiter import Limiter, RateLimitExceeded
from flask_login import current_user
from flask_security import auth_token_required

from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, TOKEN_TTL_KEY_NAME
from monkey_island.cc.flask_utils import AbstractResource, responses

from ..authentication_facade import AuthenticationFacade
from .agent_otp_login import MAX_OTP_LOGIN_REQUESTS_PER_SECOND

logger = logging.getLogger(__name__)

# We're assuming that whatever agents registered with the island simultaneously will more or less
# request refresh tokens simultaneously.
MAX_REFRESH_AUTHENTICATION_TOKEN_REQUESTS_PER_SECOND = MAX_OTP_LOGIN_REQUESTS_PER_SECOND


class RefreshAuthenticationToken(AbstractResource):
    """
    A resource for refreshing tokens
    """

    urls = ["/api/refresh-authentication-token"]
    lock = Lock()
    limiter = None

    def __init__(self, authentication_facade: AuthenticationFacade, limiter: Limiter):
        # Since flask generates a new instance of this class for each request,
        # we need to ensure that a single instance of the limiter is used. Hence
        # the class variable.
        with RefreshAuthenticationToken.lock:
            if RefreshAuthenticationToken.limiter is None:
                RefreshAuthenticationToken.limiter = limiter.limit(
                    f"{MAX_REFRESH_AUTHENTICATION_TOKEN_REQUESTS_PER_SECOND}/second",
                    key_func=lambda: current_user.username,
                    per_method=True,
                )

        self._authentication_facade = authentication_facade

    @auth_token_required
    def post(self):
        """
        Returns a new token for the authenticated user

        :return: Response with a new token or an invalid request response
        """
        if RefreshAuthenticationToken.limiter is None:
            raise RuntimeError("limiter has not been initialized")

        try:
            with RefreshAuthenticationToken.limiter:
                return self._handle_refresh_authentication_token_request()
        except RateLimitExceeded:
            return make_response("Rate limit exceeded", HTTPStatus.TOO_MANY_REQUESTS)

    def _handle_refresh_authentication_token_request(self):
        try:
            new_token, token_ttl_sec = self._authentication_facade.refresh_user_token(current_user)
            response = {
                "response": {
                    "user": {
                        ACCESS_TOKEN_KEY_NAME: new_token.get_secret_value(),
                        TOKEN_TTL_KEY_NAME: token_ttl_sec,
                    }
                }
            }
            return response, HTTPStatus.OK
        except Exception:
            return responses.make_response_to_invalid_request()

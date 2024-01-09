import string
from http import HTTPStatus
from threading import Lock
from typing import Tuple

from flask import make_response, request
from flask_limiter import Limiter, RateLimitExceeded
from flask_limiter.util import get_remote_address
from monkeytoolbox import secure_generate_random_string
from monkeytypes import OTP, AgentID

from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, TOKEN_TTL_KEY_NAME
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole

from ..authentication_facade import AuthenticationFacade
from .utils import include_auth_token

# 100 requests per second is arbitrary, but is expected to be a good-enough limit. Remember that,
# because of the agent's relay/tunnel capability, many requests could be funneled through the same
# agent's relay, making them appear to come from the same IP.
MAX_OTP_LOGIN_REQUESTS_PER_SECOND = 100


class ArgumentParsingException(Exception):
    pass


class AgentOTPLogin(AbstractResource):
    """
    A resource for logging in using an OTP

    A client may authenticate with the Island by providing a one-time password.
    """

    urls = ["/api/agent-otp-login"]
    lock = Lock()
    limiter = None

    def __init__(self, authentication_facade: AuthenticationFacade, limiter: Limiter):
        # Since flask generates a new instance of this class for each request,
        # we need to ensure that a single instance of the limiter is used. Hence
        # the class variable.
        with AgentOTPLogin.lock:
            if AgentOTPLogin.limiter is None:
                AgentOTPLogin.limiter = limiter.limit(
                    f"{MAX_OTP_LOGIN_REQUESTS_PER_SECOND}/second",
                    key_func=get_remote_address,
                    per_method=True,
                )

        self._authentication_facade = authentication_facade

    # Secured via OTP, not via authentication token.
    @include_auth_token
    def post(self):
        """
        Gets the one-time password from the request, and returns an authentication token for a
        particular Agent

        :return: Authentication token in the response body
        """
        if AgentOTPLogin.limiter is None:
            raise RuntimeError("limiter has not been initialized")

        try:
            with AgentOTPLogin.limiter:
                return self._handle_otp_login_request()
        except RateLimitExceeded:
            return make_response("Rate limit exceeded", HTTPStatus.TOO_MANY_REQUESTS)

    def _handle_otp_login_request(self):
        try:
            agent_id, otp = self._get_request_arguments(request.json)
        except ArgumentParsingException as err:
            return make_response(str(err), HTTPStatus.BAD_REQUEST)

        if not self._authentication_facade.authorize_otp(otp):
            return make_response({}, HTTPStatus.UNAUTHORIZED)

        agent_user = self._authentication_facade.create_user(
            username=str(agent_id),
            password=secure_generate_random_string(
                32, string.digits + string.ascii_letters + string.punctuation
            ),
            roles=[AccountRole.AGENT.name],
        )

        auth_token = agent_user.get_auth_token()

        return make_response(
            {
                "response": {
                    "user": {
                        ACCESS_TOKEN_KEY_NAME: auth_token,
                        TOKEN_TTL_KEY_NAME: self._authentication_facade.token_ttl_sec,
                    }
                }
            }
        )

    def _get_request_arguments(self, request_data) -> Tuple[AgentID, OTP]:
        try:
            try:
                agent_id_argument = request_data["agent_id"]
                agent_id = AgentID(agent_id_argument)
            except ValueError as err:
                raise ArgumentParsingException(f'Invalid Agent ID "{agent_id_argument}": {err}')

            try:
                otp_argument = request_data["otp"]
                otp = OTP(otp_argument)
            except ValueError as err:
                raise ArgumentParsingException(f'Invalid OTP "{otp_argument}": {err}')
        except KeyError as err:
            raise ArgumentParsingException(f"Missing argument: {err}")
        except TypeError:
            raise ArgumentParsingException("Could not parse the login request")

        return agent_id, otp

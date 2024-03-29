from http import HTTPStatus
from threading import Lock

from flask import make_response
from flask_limiter import Limiter, RateLimitExceeded
from flask_login import current_user
from flask_security import auth_token_required, roles_accepted

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole

from ..i_otp_generator import IOTPGenerator

MAX_OTP_REQUESTS_PER_SECOND = 50


class AgentOTP(AbstractResource):
    """
    A resource for requesting an Agent's one-time password

    One-time passwords may be requested by an Agent that has already authenticated,
    so that Agents that it propagates can authenticate with the Island.
    """

    urls = ["/api/agent-otp"]
    lock = Lock()
    limiter = None

    def __init__(self, otp_generator: IOTPGenerator, limiter: Limiter):
        # Since flask generates a new instance of this class for each request,
        # we need to ensure that a single instance of the limiter is used. Hence
        # the class variable.
        #
        # Note that we do not want to limit to just per-user, otherwise this endpoint could be used
        # to enumerate users/tokens. This should already be captured by the role-based access
        # control.
        with AgentOTP.lock:
            if AgentOTP.limiter is None:
                AgentOTP.limiter = limiter.limit(
                    f"{MAX_OTP_REQUESTS_PER_SECOND}/second",
                    key_func=lambda: current_user.username,
                    per_method=True,
                )

        self._otp_generator = otp_generator

    @auth_token_required
    @roles_accepted(AccountRole.AGENT.name, AccountRole.ISLAND_INTERFACE.name)
    def get(self):
        """
        Requests an Agent's one-time password

        :return: One-time password in the response body
        """
        if AgentOTP.limiter is None:
            raise RuntimeError("limiter has not been initialized")
        try:
            with AgentOTP.limiter:
                return make_response({"otp": self._otp_generator.generate_otp().get_secret_value()})
        except RateLimitExceeded:
            return make_response("Rate limit exceeded", HTTPStatus.TOO_MANY_REQUESTS)

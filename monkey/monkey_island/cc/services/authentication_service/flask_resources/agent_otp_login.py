import json

from flask import make_response, request
from flask_security import RegisterForm
from flask_security.registerable import register_user

from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, REFRESH_TOKEN_KEY_NAME
from common.types import AgentID
from common.utils.code_utils import secure_generate_random_string
from monkey_island.cc.flask_utils import AbstractResource, responses
from monkey_island.cc.services.authentication_service import AccountRole

from ..authentication_facade import AuthenticationFacade
from ..types import OTP
from .utils import include_auth_token


class AgentOTPLogin(AbstractResource):
    """
    A resource for logging in using an OTP

    A client may authenticate with the Island by providing a one-time password.
    """

    urls = ["/api/agent-otp-login/<uuid:agent_id>"]

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    @include_auth_token
    def post(self, agent_id: AgentID):
        """
        Gets the one-time password from the request,
        and returns an authentication token and a refresh token
        for a particular Agent

        :param agent_id: The ID of the Agent trying to log in
        :return: Authentication token in the response body
        """

        try:
            otp = json.loads(request.data).get("otp", "")
            if self._validate_otp(otp):
                agent_user = register_user(
                    RegisterForm(
                        username=str(agent_id),
                        password=secure_generate_random_string(32),
                        roles=[AccountRole.AGENT.name],
                    )
                )

                auth_token = agent_user.get_auth_token()
                refresh_token = self._authentication_facade.generate_refresh_token(agent_user)

                return make_response(
                    {
                        "response": {
                            "user": {
                                ACCESS_TOKEN_KEY_NAME: auth_token,
                                REFRESH_TOKEN_KEY_NAME: refresh_token,
                            }
                        }
                    }
                )

        except Exception:
            return responses.make_response_to_invalid_request()

    def _validate_otp(self, otp: OTP):
        return len(otp) > 0

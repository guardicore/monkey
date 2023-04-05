import string
from http import HTTPStatus
from typing import Tuple

from flask import make_response, request
from flask_security import RegisterForm
from flask_security.registerable import register_user

from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, REFRESH_TOKEN_KEY_NAME
from common.types import AgentID
from common.utils.code_utils import secure_generate_random_string
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole

from ..authentication_facade import AuthenticationFacade
from ..types import OTP


class ArgumentParsingException(Exception):
    pass


class AgentOTPLogin(AbstractResource):
    """
    A resource for logging in using an OTP

    A client may authenticate with the Island by providing a one-time password.
    """

    urls = ["/api/agent-otp-login"]

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    def post(self):
        """
        Gets the one-time password from the request,
        and returns an authentication token and a refresh token
        for a particular Agent

        :return: Authentication token and refresh token in the response body
        """
        try:
            agent_id, otp = self._get_request_arguments(request.json)
        except ArgumentParsingException as err:
            return make_response(str(err), HTTPStatus.BAD_REQUEST)

        if not self._authentication_facade.authorize_otp(otp):
            return make_response({}, HTTPStatus.UNAUTHORIZED)

        agent_user = register_user(
            RegisterForm(
                username=str(agent_id),
                password=secure_generate_random_string(
                    32, string.digits + string.ascii_letters + string.punctuation
                ),
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

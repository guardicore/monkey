import json

from flask import make_response, request

from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME
from monkey_island.cc.flask_utils import AbstractResource, responses

from ..authentication_facade import AuthenticationFacade
from ..types import OTP
from .utils import add_refresh_token_to_response


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

        :return: Authentication token in the response body
        """

        try:
            cred_dict = json.loads(request.data)
            otp = cred_dict.get("otp", "")
            if self._validate_otp(otp):
                refresh_token = "refreshtoken"

                response = make_response(
                    {"response": {"user": {ACCESS_TOKEN_KEY_NAME: "supersecrettoken"}}}
                )
                response = add_refresh_token_to_response(response, refresh_token)

                return response

        except Exception:
            pass

        return responses.make_response_to_invalid_request()

    def _validate_otp(self, otp: OTP):
        return len(otp) > 0

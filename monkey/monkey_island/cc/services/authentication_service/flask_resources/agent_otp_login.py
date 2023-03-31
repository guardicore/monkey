import json

from flask import make_response, request
from flask_login import current_user

from monkey_island.cc.flask_utils import AbstractResource, responses

from ..authentication_facade import AuthenticationFacade


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
                response_data = {"authentication_token": "supersecrettoken"}
                response_data["refresh_token"] = self._authentication_facade.generate_refresh_token(
                    current_user
                )
                return make_response(response_data)

        except Exception:
            pass

        return responses.make_response_to_invalid_request()

    def _validate_otp(self, otp: str):
        return len(otp) > 0

import json

from flask import make_response, request

from monkey_island.cc.flask_utils import AbstractResource, responses


class AgentOTPLogin(AbstractResource):
    """
    A resource for logging in using an OTP

    A client may authenticate with the Island by providing a one-time password.
    """

    urls = ["/api/agent-otp-login"]

    def post(self):
        """
        Gets the one-time password from the request, and returns an authentication token

        :return: Authentication token in the response body
        """

        try:
            cred_dict = json.loads(request.data)
            otp = cred_dict.get("otp", "")
            if self._validate_otp(otp):
                return make_response({"token": "supersecrettoken"})
        except Exception:
            pass

        return responses.make_response_to_invalid_request()

    def _validate_otp(self, otp: str):
        return len(otp) > 0

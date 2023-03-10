from flask import make_response

from monkey_island.cc.flask_utils import AbstractResource


class AgentOTP(AbstractResource):
    """
    A resource for requesting an Agent's one-time password

    One-time passwords may be requested by an Agent that has already authenticated,
    so that Agents that it propagates can authenticate with the Island.
    """

    urls = ["/api/agent-otp"]

    def get(self):
        """
        Requests an Agent's one-time password

        :return: One-time password in the response body
        """

        return make_response({"otp": "supersecretpassword"})

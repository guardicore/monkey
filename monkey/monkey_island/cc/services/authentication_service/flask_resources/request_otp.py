from flask import make_response

from monkey_island.cc.flask_utils import AbstractResource


class RequestOTP(AbstractResource):
    """
    A resource for requesting a one-time password

    One-time passwords may be requested by an Agent that has already authenticated,
    so that Agents that it propagates can register.
    """

    urls = ["/api/request-otp"]

    def get(self):
        """
        Requests a one-time password

        :return: One-time password in the response body
        """

        return make_response({"otp": "supersecretpassword"})

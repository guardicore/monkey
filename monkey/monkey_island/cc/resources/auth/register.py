import logging
from http import HTTPStatus

from flask import make_response, request
from flask.typing import ResponseValue
from flask_security.views import register

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.resources.auth.credential_utils import get_username_password_from_request
from monkey_island.cc.services.authentication_service import AuthenticationService

logger = logging.getLogger(__name__)


class Register(AbstractResource):
    """
    A resource for user registration
    """

    urls = ["/api/register"]

    def __init__(self, authentication_service: AuthenticationService):
        self._authentication_service = authentication_service

    def post(self):
        """
        Registers a new user using flask security register

        """
        try:
            username, password = get_username_password_from_request(request)
            if not username or not password:
                return make_response(
                    {"error": "Provided empty credentials"}, HTTPStatus.BAD_REQUEST
                )

            # This method take the request data and pass it to the RegisterForm
            # where a registration request is preform.
            # Return value is a flask.Response object
            response: ResponseValue = register()

            if response.status_code == HTTPStatus.OK:
                self._authentication_service.reset_island(username, password)

            return make_response(response)
        except Exception as err:
            return make_response({"error": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR)

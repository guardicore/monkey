import logging
from http import HTTPStatus

from flask import make_response, request

from common.utils.exceptions import AlreadyRegisteredError, InvalidRegistrationCredentialsError
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.resources.auth.credential_utils import get_username_password_from_request
from monkey_island.cc.services import AuthenticationService

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
        Registers a new user

        Gets a username and password from the request sent from the client,
        and registers a new user

        :raises InvalidRegistrationCredentialsError: If username or password is empty
        :raises AlreadyRegisteredError: If a user has already been registered
        """

        username, password = get_username_password_from_request(request)

        try:
            self._authentication_service.register_new_user(username, password)
            return make_response({"error": ""}, HTTPStatus.OK)
        # API Spec: HTTP status code for AlreadyRegisteredError should be 409 (CONFLICT)
        except (InvalidRegistrationCredentialsError, AlreadyRegisteredError) as e:
            return make_response({"error": str(e)}, HTTPStatus.BAD_REQUEST)

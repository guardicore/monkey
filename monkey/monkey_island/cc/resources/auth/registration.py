import logging
from http import HTTPStatus

from flask import make_response, request

from common.utils.exceptions import AlreadyRegisteredError, InvalidRegistrationCredentialsError
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.auth.credential_utils import get_username_password_from_request
from monkey_island.cc.services import AuthenticationService

logger = logging.getLogger(__name__)


class Registration(AbstractResource):

    urls = ["/api/registration"]

    def __init__(self, authentication_service: AuthenticationService):
        self._authentication_service = authentication_service

    def get(self):
        return {"needs_registration": self._authentication_service.needs_registration()}

    def post(self):
        username, password = get_username_password_from_request(request)

        try:
            self._authentication_service.register_new_user(username, password)
            return make_response({"error": ""}, HTTPStatus.OK)
        # API Spec: HTTP status code for AlreadyRegisteredError should be 409 (CONFLICT)
        # API Spec: HTTP status code for InvalidRegistrationCredentialsError should be 401
        #           (UNAUTHORIZED). See https://www.rfc-editor.org/rfc/rfc7235#section-3.1
        except (InvalidRegistrationCredentialsError, AlreadyRegisteredError) as e:
            return make_response({"error": str(e)}, HTTPStatus.BAD_REQUEST)

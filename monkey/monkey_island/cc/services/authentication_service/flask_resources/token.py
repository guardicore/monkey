import logging
from http import HTTPStatus

from flask import request

from monkey_island.cc.flask_utils import AbstractResource, responses

from ..authentication_facade import AuthenticationFacade
from .utils import ACCESS_TOKEN_KEY_NAME, REFRESH_TOKEN_KEY_NAME

logger = logging.getLogger(__name__)


class Token(AbstractResource):
    """
    A resource for user authentication
    """

    urls = ["/api/token"]

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    def post(self):
        """
        Accepts a refresh token and returns a new token pair

        :return: Access token in the response body
        :raises IncorrectCredentialsError: If credentials are invalid
        """
        try:
            old_refresh_token = request.json[REFRESH_TOKEN_KEY_NAME]
            access_token, refresh_token = self._authentication_facade.generate_new_token_pair(
                old_refresh_token
            )
            response = {
                "response": {
                    "user": {
                        ACCESS_TOKEN_KEY_NAME: access_token,
                        REFRESH_TOKEN_KEY_NAME: refresh_token,
                    }
                }
            }
            return response, HTTPStatus.OK
        except Exception:
            return responses.make_response_to_invalid_request()

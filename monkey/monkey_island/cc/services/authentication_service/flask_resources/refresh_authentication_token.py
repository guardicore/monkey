import logging
from http import HTTPStatus

from flask import make_response, request

from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, REFRESH_TOKEN_KEY_NAME
from monkey_island.cc.flask_utils import AbstractResource, responses
from monkey_island.cc.services.authentication_service.token_parser import TokenValidationError

from ..authentication_facade import AuthenticationFacade

logger = logging.getLogger(__name__)


class RefreshAuthenticationToken(AbstractResource):
    """
    A resource for refreshing tokens
    """

    urls = ["/api/refresh-authentication-token"]

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    # TODO: Decorate after "user-refresh" logic is added
    def post(self):
        """
        Accepts a refresh token and returns a new token pair

        :return: Response with new token pair or an invalid request response
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
        except TokenValidationError:
            return make_response({}, HTTPStatus.UNAUTHORIZED)
        except Exception:
            return responses.make_response_to_invalid_request()

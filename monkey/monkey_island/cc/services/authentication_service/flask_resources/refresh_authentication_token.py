import logging
from http import HTTPStatus

from flask_login import current_user
from flask_security import auth_token_required

from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, TOKEN_TTL_KEY_NAME
from monkey_island.cc.flask_utils import AbstractResource, responses

from ..authentication_facade import AuthenticationFacade

logger = logging.getLogger(__name__)


class RefreshAuthenticationToken(AbstractResource):
    """
    A resource for refreshing tokens
    """

    urls = ["/api/refresh-authentication-token"]

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    @auth_token_required
    def post(self):
        """
        Returns a new token for the authenticated user

        :return: Response with a new token or an invalid request response
        """
        try:
            new_token, token_ttl_sec = self._authentication_facade.refresh_user_token(current_user)
            response = {
                "response": {
                    "user": {
                        ACCESS_TOKEN_KEY_NAME: new_token.get_secret_value(),
                        TOKEN_TTL_KEY_NAME: token_ttl_sec,
                    }
                }
            }
            return response, HTTPStatus.OK
        except Exception:
            return responses.make_response_to_invalid_request()

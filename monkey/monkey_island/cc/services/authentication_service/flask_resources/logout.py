import logging
from http import HTTPStatus

from flask import Response, make_response
from flask.typing import ResponseValue
from flask_login import current_user
from flask_security import auth_token_required, roles_accepted
from flask_security.views import logout

from monkey_island.cc.flask_utils import AbstractResource, responses
from monkey_island.cc.services.authentication_service import AccountRole
from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)

logger = logging.getLogger(__name__)


class Logout(AbstractResource):
    """
    A resource logging out an authenticated user
    """

    urls = ["/api/logout"]

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    @auth_token_required
    @roles_accepted(AccountRole.AGENT.name, AccountRole.ISLAND_INTERFACE.name)
    def post(self):
        user_is_agent = False
        try:
            self._authentication_facade.revoke_all_tokens_for_user(current_user)
            username = current_user.username
            user_is_agent = current_user.has_role(AccountRole.AGENT.name)
            response: ResponseValue = logout()
        except Exception:
            return responses.make_response_to_invalid_request()

        if not isinstance(response, Response):
            return responses.make_response_to_invalid_request()

        if response.status_code == HTTPStatus.OK:
            if user_is_agent:
                self._authentication_facade.remove_user(username)

        return make_response(response)

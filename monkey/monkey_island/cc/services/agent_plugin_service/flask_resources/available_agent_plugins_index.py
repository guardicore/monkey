import logging
from http import HTTPStatus

from flask import make_response
from flask_security import auth_token_required, roles_accepted

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole

from .. import IAgentPluginService

logger = logging.getLogger(__name__)


class AvailableAgentPluginsIndex(AbstractResource):
    urls = ["/api/agent-plugins/available/index"]

    def __init__(self, agent_plugin_service: IAgentPluginService):
        self._agent_plugin_service = agent_plugin_service

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def get(self):
        """
        Get the index of available plugins
        """

        available_plugins = self._agent_plugin_service.get_available_plugins()

        return make_response(available_plugins.dict(simplify=True), HTTPStatus.OK)

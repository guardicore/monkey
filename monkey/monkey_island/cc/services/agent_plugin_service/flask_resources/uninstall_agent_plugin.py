import logging
from http import HTTPStatus

from flask import make_response
from flask_security import auth_token_required, roles_accepted

from common.agent_plugins import AgentPluginType
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole

from .. import IAgentPluginService

logger = logging.getLogger(__name__)


class UninstallAgentPlugin(AbstractResource):
    urls = ["/api/uninstall-agent-plugin/<string:plugin_type>/<string:name>"]

    def __init__(self, agent_plugin_service: IAgentPluginService):
        self._agent_plugin_service = agent_plugin_service

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def post(self, plugin_type: str, name: str):
        """
        Uninstalls agent plugin of the specified type and name.

        :param plugin_type: The type of plugin (e.g. "Exploiter")
        :param name: The name of the plugin
        """
        try:
            plugin_type_ = AgentPluginType(plugin_type)
        except ValueError:
            message = f"Invalid type '{plugin_type}'."
            logger.warning(message)
            return make_response({"message": message}, HTTPStatus.NOT_FOUND)

        self._agent_plugin_service.uninstall_agent_plugin(plugin_type_, name)
        return make_response({}, HTTPStatus.OK)

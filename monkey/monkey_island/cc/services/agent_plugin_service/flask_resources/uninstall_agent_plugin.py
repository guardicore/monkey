import json
import logging
from http import HTTPStatus

from flask import make_response, request
from flask_security import auth_token_required, roles_accepted
from monkeytypes import AgentPluginType

from common.agent_plugins import PluginName
from monkey_island.cc.flask_utils import AbstractResource, responses
from monkey_island.cc.services.authentication_service import AccountRole

from .. import IAgentPluginService

logger = logging.getLogger(__name__)


class UninstallAgentPlugin(AbstractResource):
    urls = ["/api/uninstall-agent-plugin"]

    def __init__(self, agent_plugin_service: IAgentPluginService):
        self._agent_plugin_service = agent_plugin_service

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def post(self):
        """
        Uninstalls agent plugin of the specified plugin type and name.
        """
        try:
            response_json = json.loads(request.data)
            plugin_type_arg = response_json["plugin_type"]
            plugin_name_arg = response_json["name"]
        except Exception:
            return responses.make_response_to_invalid_request()

        try:
            plugin_type = AgentPluginType(plugin_type_arg)
        except ValueError:
            message = f"Invalid type '{plugin_type_arg}'."
            logger.warning(message)
            return responses.make_response_to_invalid_request(message)

        self._agent_plugin_service.uninstall_plugin(plugin_type, PluginName(plugin_name_arg))
        return make_response({}, HTTPStatus.OK)

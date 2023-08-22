import json
import logging
from http import HTTPStatus

from flask import make_response, request
from flask_security import auth_token_required, roles_accepted

from common.agent_plugins import AgentPluginType
from monkey_island.cc.flask_utils import AbstractResource, responses
from monkey_island.cc.services.authentication_service import AccountRole

from .. import IAgentPluginService
from ..errors import UninstallPluginError

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
            plugin_type = response_json["plugin_type"]
            name = response_json["name"]
        except Exception:
            return responses.make_response_to_invalid_request()

        try:
            plugin_type_ = AgentPluginType(plugin_type)
        except ValueError:
            message = f"Invalid type '{plugin_type}'."
            logger.warning(message)
            return make_response({"message": message}, HTTPStatus.NOT_FOUND)

        try:
            self._agent_plugin_service.uninstall_agent_plugin(plugin_type_, name)
        except UninstallPluginError as err:
            return make_response(str(err), HTTPStatus.UNPROCESSABLE_ENTITY)
        return make_response({}, HTTPStatus.OK)

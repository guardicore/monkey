import json
import logging
from http import HTTPStatus

from flask import make_response, request
from flask_security import auth_token_required, roles_accepted

from common.agent_plugins import AgentPluginType, PluginName, PluginVersion
from monkey_island.cc.flask_utils import AbstractResource, responses
from monkey_island.cc.services.authentication_service import AccountRole

from .. import IAgentPluginService
from ..errors import PluginInstallationError

logger = logging.getLogger(__name__)


class InstallAgentPlugin(AbstractResource):
    urls = ["/api/install-agent-plugin"]

    def __init__(self, agent_plugin_service: IAgentPluginService):
        self._agent_plugin_service = agent_plugin_service

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def put(self):
        """
        Install the plugin archive.
        """
        try:
            content_type = request.headers.get("Content-Type", "").lower()
            if content_type == "application/json":
                try:
                    self._handle_json_request()
                except ValueError:
                    message = "Invalid plugin type."
                    logger.warning(message)
                    return responses.make_response_to_invalid_request(message)
                except Exception:
                    return responses.make_response_to_invalid_request()
            else:
                self._agent_plugin_service.install_plugin_archive(request.data)
            return make_response({}, HTTPStatus.OK)
        except PluginInstallationError as err:
            return make_response(str(err), HTTPStatus.UNPROCESSABLE_ENTITY)

    def _handle_json_request(self):
        response_json = json.loads(request.data)
        plugin_type = response_json["plugin_type"]
        name = response_json["name"]
        version = response_json["version"]

        plugin_type_ = AgentPluginType(plugin_type)
        plugin_name = PluginName(name)
        plugin_version = PluginVersion(version)

        self._agent_plugin_service.install_plugin_from_repository(
            plugin_type=plugin_type_, plugin_name=plugin_name, plugin_version=plugin_version
        )

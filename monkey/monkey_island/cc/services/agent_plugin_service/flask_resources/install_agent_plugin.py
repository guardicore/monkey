import json
import logging
from http import HTTPStatus
from typing import Tuple

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
                    (
                        plugin_type,
                        plugin_name,
                        plugin_version,
                    ) = self._get_plugin_information_from_request()
                except Exception as err:
                    logger.warning(err)
                    return responses.make_response_to_invalid_request(str(err))

                self._agent_plugin_service.install_plugin_from_repository(
                    plugin_type=plugin_type, plugin_name=plugin_name, plugin_version=plugin_version
                )
            else:
                self._agent_plugin_service.install_plugin_archive(request.data)
            return make_response({}, HTTPStatus.OK)
        except PluginInstallationError as err:
            return make_response(str(err), HTTPStatus.UNPROCESSABLE_ENTITY)

    def _get_plugin_information_from_request(
        self,
    ) -> Tuple[AgentPluginType, PluginName, PluginVersion]:
        response_json = json.loads(request.data)
        plugin_type_arg = response_json["plugin_type"]
        plugin_name_arg = response_json["name"]
        plugin_version_arg = response_json["version"]

        plugin_name = PluginName(plugin_name_arg)
        try:
            plugin_type = AgentPluginType(plugin_type_arg)
        except ValueError:
            message = f"Invalid plugin type argument: {plugin_type_arg}."
            raise ValueError(message)

        try:
            plugin_version = PluginVersion.from_str(plugin_version_arg)
        except ValueError as err:
            message = f"Invalid plugin version argument: {plugin_version_arg}: {err}."
            raise ValueError(message)

        return plugin_type, plugin_name, plugin_version

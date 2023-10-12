import logging
from http import HTTPStatus

from flask import make_response
from flask_security import auth_token_required, roles_accepted
from monkeytypes import AgentPluginManifest, AgentPluginType

from common.agent_plugins import PluginName
from common.hard_coded_manifests.hard_coded_fingerprinter_manifests import (
    HARD_CODED_FINGERPRINTER_MANIFESTS,
)
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole

from .. import IAgentPluginService

logger = logging.getLogger(__name__)


class AgentPluginsManifest(AbstractResource):
    urls = ["/api/agent-plugins/<string:plugin_type>/<string:name>/manifest"]

    def __init__(self, agent_plugin_service: IAgentPluginService):
        self._agent_plugin_service = agent_plugin_service

    @auth_token_required
    @roles_accepted(AccountRole.AGENT.name)
    def get(self, plugin_type: str, name: str):
        """
        Get the plugin manifest of the specified type and name.

        :param plugin_type: The type of plugin (e.g. "Exploiter")
        :param name: The name of the plugin
        """
        try:
            plugin_type_ = AgentPluginType(plugin_type)
        except ValueError:
            message = f"Invalid type '{plugin_type}'."
            logger.warning(message)
            return make_response({"message": message}, HTTPStatus.NOT_FOUND)

        try:
            plugin_manifest = self._get_plugin_manifest(plugin_type_, PluginName(name))
        except KeyError:
            message = f"Plugin '{name}' of type '{plugin_type_}' not found."
            logger.warning(message)
            return make_response({"message": message}, HTTPStatus.NOT_FOUND)

        return make_response(plugin_manifest.model_dump(mode="json"), HTTPStatus.OK)

    def _get_plugin_manifest(
        self, plugin_type: AgentPluginType, name: PluginName
    ) -> AgentPluginManifest:
        plugin_manifests = self._agent_plugin_service.get_all_plugin_manifests()
        try:
            return plugin_manifests[plugin_type][name]
        except KeyError as err:
            if plugin_type == AgentPluginType.FINGERPRINTER:
                return HARD_CODED_FINGERPRINTER_MANIFESTS[name]
            else:
                raise err

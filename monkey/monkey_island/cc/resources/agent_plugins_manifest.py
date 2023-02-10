import logging
from http import HTTPStatus

from flask import make_response

from common import HARD_CODED_EXPLOITER_MANIFESTS
from common.agent_plugins import AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories import IAgentPluginRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource

logger = logging.getLogger(__name__)


class AgentPluginsManifest(AbstractResource):
    urls = ["/api/agent-plugins/<string:plugin_type>/<string:name>/manifest"]

    def __init__(self, agent_plugin_repository: IAgentPluginRepository):
        self._agent_plugin_repository = agent_plugin_repository

    # Used by monkey. can't secure.
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
            plugin_manifest = self._get_plugin_manifest(plugin_type_, name)
        except KeyError:
            message = f"Plugin '{name}' of type '{plugin_type_}' not found."
            logger.warning(message)
            return make_response({"message": message}, HTTPStatus.NOT_FOUND)

        return make_response(plugin_manifest.dict(simplify=True), HTTPStatus.OK)

    def _get_plugin_manifest(self, plugin_type: AgentPluginType, name: str) -> AgentPluginManifest:
        plugin_manifests = self._agent_plugin_repository.get_all_plugin_manifests()
        try:
            return plugin_manifests[plugin_type][name]
        except KeyError as err:
            if plugin_type == AgentPluginType.EXPLOITER:
                return HARD_CODED_EXPLOITER_MANIFESTS[name]
            else:
                raise err

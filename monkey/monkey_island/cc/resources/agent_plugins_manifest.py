import logging
from http import HTTPStatus

from flask import make_response

from common.agent_plugins import AgentPluginType
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

        :param type: The type of plugin (e.g. Exploiter)
        :param name: The name of the plugin
        """
        try:
            agent_plugin_type = AgentPluginType(plugin_type)
        except ValueError:
            message = f"Invalid type '{plugin_type}'."
            logger.warning(message)
            return make_response({"message": message}, HTTPStatus.NOT_FOUND)

        try:
            plugin_manifests = self._agent_plugin_repository.get_all_plugin_manifests()
            agent_plugin_manifest = plugin_manifests[agent_plugin_type][name]
            return make_response(agent_plugin_manifest.dict(simplify=True), HTTPStatus.OK)
        except KeyError:
            message = f"Plugin '{name}' of type '{plugin_type}' not found."
            logger.warning(message)
            return make_response({"message": message}, HTTPStatus.NOT_FOUND)

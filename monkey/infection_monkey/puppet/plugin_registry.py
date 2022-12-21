import logging
from copy import copy
from typing import Any, Dict

from serpentarium import PluginLoader, SingleUsePlugin

from common.agent_plugins import AgentPlugin, AgentPluginType
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIRequestError

from . import PluginSourceExtractor

logger = logging.getLogger()


class PluginRegistry:
    def __init__(
        self,
        island_api_client: IIslandAPIClient,
        plugin_source_extractor: PluginSourceExtractor,
        plugin_loader: PluginLoader,
    ):
        """
        `self._registry` looks like -
            {
                AgentPluginType.EXPLOITER: {
                    "ZerologonExploiter": ZerologonExploiter,
                    "SMBExploiter": SMBExploiter
                }
            }
        """
        self._registry: Dict[AgentPluginType, Dict[str, SingleUsePlugin]] = {}
        self._island_api_client = island_api_client
        self._plugin_source_extractor = plugin_source_extractor
        self._plugin_loader = plugin_loader

    def load_plugin(self, plugin_name: str, plugin: object, plugin_type: AgentPluginType) -> None:
        self._registry.setdefault(plugin_type, {})
        self._registry[plugin_type][plugin_name] = plugin

        logger.debug(f"Plugin '{plugin_name}' loaded")

    def get_plugin(self, plugin_name: str, plugin_type: AgentPluginType) -> Any:
        try:
            return copy(self._registry[plugin_type][plugin_name])
        except KeyError:
            self._load_plugin_from_island(plugin_name, plugin_type)
            return copy(self._registry[plugin_type][plugin_name])

    def _load_plugin_from_island(self, plugin_name: str, plugin_type: AgentPluginType):
        agent_plugin = self._download_plugin_from_island(plugin_name, plugin_type)
        self._plugin_source_extractor.extract_plugin_source(agent_plugin)
        multiprocessing_plugin = self._plugin_loader.load_multiprocessing_plugin(
            plugin_name=plugin_name
        )

        self.load_plugin(plugin_name, multiprocessing_plugin, plugin_type)

    def _download_plugin_from_island(
        self, plugin_name: str, plugin_type: AgentPluginType
    ) -> AgentPlugin:
        try:
            plugin = self._island_api_client.get_agent_plugin(plugin_type, plugin_name)
        except IslandAPIRequestError as err:
            raise UnknownPluginError(
                f"Unknown plugin '{plugin_name}' of type '{plugin_type.value}': {err}"
            )

        logger.debug(f"Plugin '{plugin_name}' downloaded from the island")
        return plugin

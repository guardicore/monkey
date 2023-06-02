import logging
from copy import copy
from threading import RLock
from typing import Dict

from serpentarium import SingleUsePlugin

from common import OperatingSystem
from common.agent_event_serializers import AgentEventSerializerRegistry
from common.agent_plugins import AgentPlugin, AgentPluginType, PluginSourceExtractor
from common.agent_plugins.plugin_events_loader import get_plugin_event_classes
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIRequestError
from infection_monkey.plugin.i_plugin_factory import IPluginFactory

logger = logging.getLogger()


class PluginRegistry:
    def __init__(
        self,
        operating_system: OperatingSystem,
        island_api_client: IIslandAPIClient,
        plugin_source_extractor: PluginSourceExtractor,
        plugin_factories: Dict[AgentPluginType, IPluginFactory],
        agent_event_serializer_registry: AgentEventSerializerRegistry,
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

        self._operating_system = operating_system
        self._island_api_client = island_api_client
        self._plugin_source_extractor = plugin_source_extractor
        self._plugin_factories = plugin_factories
        self._agent_event_serializer_registry = agent_event_serializer_registry

        self._lock = RLock()

    def get_plugin(self, plugin_type: AgentPluginType, plugin_name: str) -> SingleUsePlugin:
        """
        Retrieve a plugin stored in the registry. If the plugin does not exist in the registry, an
        attempt will be made to download it from the island.

        :param plugin_type: The type of plugin to get.
        :param plugin_name: The name of the plugin to get.
        :return: A plugin of the given type and name.
        :raises UnknownPluginError: If the plugin is not found.
        """
        with self._lock:
            try:
                # Note: The MultiprocessingPluginWrapper is a MultiUsePlugin. The copy() used here
                # will be unnecessary once all functionality is encapsulated in plugins.
                return copy(self._registry[plugin_type][plugin_name])
            except KeyError:
                self._load_plugin_from_island(plugin_name, plugin_type)
                return copy(self._registry[plugin_type][plugin_name])

    def _load_plugin_from_island(self, plugin_name: str, plugin_type: AgentPluginType):
        agent_plugin = self._download_plugin_from_island(plugin_name, plugin_type)
        self._plugin_source_extractor.extract_plugin_source(agent_plugin)

        plugin_event_names = agent_plugin.plugin_manifest.custom_events
        if plugin_event_names is not None:
            plugin_dir = self._plugin_source_extractor.plugin_destination_directory

            # This is needed in order to load the plugin events module in the main process
            get_plugin_event_classes(plugin_name, plugin_dir, plugin_event_names)

            # This is needed in order for the events to be present in the Manager process
            self._agent_event_serializer_registry.load_plugin_events(plugin_name, plugin_dir)

        if plugin_type in self._plugin_factories:
            factory = self._plugin_factories[plugin_type]
            multiprocessing_plugin = factory.create(plugin_name)
        else:
            raise UnknownPluginError(
                "Loading of custom plugins has not been implemented for plugin type "
                f"'{plugin_type.value}'"
            )

        self.load_plugin(plugin_type, plugin_name, multiprocessing_plugin)

    def _download_plugin_from_island(
        self, plugin_name: str, plugin_type: AgentPluginType
    ) -> AgentPlugin:
        try:
            plugin = self._island_api_client.get_agent_plugin(
                self._operating_system, plugin_type, plugin_name
            )
        except IslandAPIRequestError as err:
            raise UnknownPluginError(
                f"Unknown plugin '{plugin_name}' of type '{plugin_type.value}': {err}"
            )

        logger.debug(f"Plugin '{plugin_name}' downloaded from the island")
        return plugin

    def load_plugin(self, plugin_type: AgentPluginType, plugin_name: str, plugin: object) -> None:
        with self._lock:
            self._registry.setdefault(plugin_type, {})

        self._registry[plugin_type][plugin_name] = plugin
        logger.debug(f"Plugin '{plugin_name}' loaded")

from typing import Sequence, Tuple

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginType
from monkey_island.cc.repositories import IAgentPluginRepository, UnknownRecordError


class InMemoryAgentPluginRepository(IAgentPluginRepository):
    def __init__(self):
        self._plugins = {}

    def get_plugin(self, plugin_type: AgentPluginType, name: str) -> AgentPlugin:
        if name not in self._plugins:
            raise UnknownRecordError(f"Plugin '{name}' does not exist.")
        return self._plugins[name]

    def get_plugin_for_os(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        plugin = self.get_plugin(plugin_type, name)
        if host_operating_system not in plugin.host_operating_systems:
            raise UnknownRecordError(
                f"OS '{host_operating_system}' does not exist for plugin '{name}'."
            )
        return plugin

    def get_plugin_catalog(self) -> Sequence[Tuple[AgentPluginType, str, Tuple[OperatingSystem]]]:
        return [
            (
                plugin.plugin_manifest.plugin_type,
                plugin.plugin_manifest.name,
                plugin.host_operating_systems,
            )
            for plugin in self._plugins.values()
        ]

    def save_plugin(self, plugin: AgentPlugin):
        self._plugins[plugin.plugin_manifest.name] = plugin

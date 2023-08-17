from typing import Any, Dict, Optional

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories import RetrievalError, UnknownRecordError
from monkey_island.cc.services.agent_plugin_service.i_agent_plugin_repository import (
    IAgentPluginRepository,
)


class InMemoryAgentPluginRepository(IAgentPluginRepository):
    def __init__(self):
        self._plugins = {}

    def get_plugin(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        if name not in self._plugins:
            raise UnknownRecordError(f"Plugin '{name}' does not exist.")
        plugin = self._plugins[name]
        if host_operating_system not in plugin.supported_operating_systems:
            raise RetrievalError(f"{host_operating_system} not supported for plugin '{name}'")
        return plugin

    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        schemas: Dict[AgentPluginType, Dict[str, Dict[str, Any]]] = {}

        for plugin in self._plugins.values():
            plugin_type = plugin.plugin_manifest.plugin_type
            schemas.setdefault(plugin_type, {})
            schemas[plugin_type][plugin.plugin_manifest.name] = plugin.config_schema

        return schemas

    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        manifests: Dict[AgentPluginType, Dict[str, AgentPluginManifest]] = {}

        for plugin in self._plugins.values():
            plugin_type = plugin.plugin_manifest.plugin_type
            manifests.setdefault(plugin_type, {})
            manifests[plugin_type][plugin.plugin_manifest.name] = plugin.plugin_manifest

        return manifests

    def store_agent_plugin(self, operating_system: OperatingSystem, agent_plugin: AgentPlugin):
        # TODO: Store it by OperatingSystem
        self._plugins[agent_plugin.plugin_manifest.name] = agent_plugin

    def remove_agent_plugin(
        self,
        operating_system: Optional[OperatingSystem],
        agent_plugin_name: str,
        agent_plugin_type: AgentPluginType,
    ):
        # TODO: Remove it with Operating System
        self._plugins.pop(agent_plugin_name, None)

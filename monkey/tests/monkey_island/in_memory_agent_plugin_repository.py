from typing import Any, Dict, List, Optional

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
        try:
            plugin = self._plugins[host_operating_system][plugin_type][name]
        except KeyError:
            raise UnknownRecordError(f"Plugin '{name}' does not exist.")

        if host_operating_system not in plugin.supported_operating_systems:
            raise RetrievalError(f"{host_operating_system} not supported for plugin '{name}'")
        return plugin

    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        schemas: Dict[AgentPluginType, Dict[str, Dict[str, Any]]] = {}

        for plugin in self._get_plugins_from_dict():
            plugin_type = plugin.plugin_manifest.plugin_type
            schemas.setdefault(plugin_type, {})
            schemas[plugin_type][plugin.plugin_manifest.name] = plugin.config_schema

        return schemas

    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        manifests: Dict[AgentPluginType, Dict[str, AgentPluginManifest]] = {}

        for plugin in self._get_plugins_from_dict():
            plugin_type = plugin.plugin_manifest.plugin_type
            manifests.setdefault(plugin_type, {})
            manifests[plugin_type][plugin.plugin_manifest.name] = plugin.plugin_manifest

        return manifests

    def _get_plugins_from_dict(self) -> List[AgentPlugin]:
        plugins = []
        for os, type_specific_plugins in self._plugins.items():
            for plugin_type, agent_plugins in type_specific_plugins.items():
                for plugin_name, agent_plugin in agent_plugins.items():
                    plugins.append(agent_plugin)

        return plugins

    def store_agent_plugin(self, operating_system: OperatingSystem, agent_plugin: AgentPlugin):
        if operating_system not in self._plugins:
            self._plugins[operating_system] = {}

        if agent_plugin.plugin_manifest.plugin_type not in self._plugins[operating_system]:
            self._plugins[operating_system][agent_plugin.plugin_manifest.plugin_type] = {}

        self._plugins[operating_system][agent_plugin.plugin_manifest.plugin_type][
            agent_plugin.plugin_manifest.name
        ] = agent_plugin

    def remove_agent_plugin(
        self,
        agent_plugin_type: AgentPluginType,
        agent_plugin_name: str,
        operating_system: Optional[OperatingSystem] = None,
    ):
        if operating_system is None:
            for os in self._plugins.keys():
                self._remove_os_specific_plugin(agent_plugin_type, agent_plugin_name, os)
        else:
            self._remove_os_specific_plugin(agent_plugin_type, agent_plugin_name, operating_system)

    def _remove_os_specific_plugin(
        self,
        agent_plugin_type: AgentPluginType,
        agent_plugin_name: str,
        operating_system: OperatingSystem,
    ):
        os_specific_plugins = self._plugins.get(operating_system, None)
        if os_specific_plugins:
            type_specific_plugins = os_specific_plugins.get(agent_plugin_type, None)
            if type_specific_plugins:
                type_specific_plugins.pop(agent_plugin_name, None)

from typing import Any, Dict, Sequence

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType

from . import IAgentPluginRepository, IFileRepository, RetrievalError
from .plugin_archive_parser import parse_plugin


class FileAgentPluginRepository(IAgentPluginRepository):
    """
    A repository for retrieving agent plugins.
    """

    def __init__(self, plugin_file_repository: IFileRepository):
        """
        :param plugin_file_repository: IFileRepository containing the plugins
        """
        self._plugin_file_repository = plugin_file_repository

    def get_plugin(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        plugin = self._get_plugin(plugin_type, name)

        if host_operating_system in plugin.host_operating_systems:
            # TODO: Return the plugin with only the operating system specific dependencies
            return plugin
        else:
            raise RetrievalError(
                f"Error retrieving the agent plugin {name} of type {plugin_type} "
                f"for OS {host_operating_system}"
            )

    def _get_plugin(self, plugin_type: AgentPluginType, name: str) -> AgentPlugin:
        plugin_file_name = f"{name}-{plugin_type.value.lower()}.tar"

        try:
            with self._plugin_file_repository.open_file(plugin_file_name) as f:
                return parse_plugin(f)
        except ValueError as err:
            raise RetrievalError(f"Error retrieving the agent plugin {plugin_file_name}: {err}")

    def get_all_plugin_config_schemas(self) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        schemas: Dict[AgentPluginType, Dict[str, Dict[str, Any]]] = {}
        for plugin in self._get_all_plugins():
            plugin_type = plugin.plugin_manifest.plugin_type
            if plugin_type not in schemas:
                schemas[plugin_type] = {}
            schemas[plugin_type][plugin.plugin_manifest.name] = plugin.config_schema

        return schemas

    def _get_all_plugins(self) -> Sequence[AgentPlugin]:
        plugins = []

        plugin_file_names = self._plugin_file_repository.get_all_file_names()
        for plugin_file_name in plugin_file_names:
            plugin_name, plugin_type = plugin_file_name.split(".")[0].split("-")

            try:
                agent_plugin_type = AgentPluginType[plugin_type.upper()]
                plugin = self._get_plugin(agent_plugin_type, plugin_name)
                plugins.append(plugin)
            except KeyError as err:
                raise RetrievalError(
                    f"Error retrieving plugin {plugin_name} of "
                    f"type {plugin_type.upper()}: {err}"
                )

        return plugins

    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        manifests: Dict[AgentPluginType, Dict[str, AgentPluginManifest]] = {}
        for plugin in self._get_all_plugins():
            plugin_type = plugin.plugin_manifest.plugin_type
            if plugin_type not in manifests:
                manifests[plugin_type] = {}
            manifests[plugin_type][plugin.plugin_manifest.name] = plugin.plugin_manifest

        return manifests

from typing import Any, Dict, List, Mapping

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
        parsed_plugin = self._load_plugin_from_file(plugin_type, name)

        if host_operating_system in parsed_plugin:
            return parsed_plugin[host_operating_system]
        else:
            raise RetrievalError(
                f"Error retrieving the agent plugin {name} of type {plugin_type} "
                f"for OS {host_operating_system}"
            )

    def _load_plugin_from_file(
        self, plugin_type: AgentPluginType, name: str
    ) -> Mapping[OperatingSystem, AgentPlugin]:
        plugin_file_name = f"{name}-{plugin_type.value.lower()}.tar"

        try:
            with self._plugin_file_repository.open_file(plugin_file_name) as f:
                return parse_plugin(f)
        except ValueError as err:
            raise RetrievalError(f"Error retrieving the agent plugin {plugin_file_name}: {err}")

    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        schemas: Dict[AgentPluginType, Dict[str, Dict[str, Any]]] = {}
        for parsed_plugin in self._get_all_plugins():
            plugin_objects = list(parsed_plugin.values())
            try:
                # doesn't matter which OS's plugin this is since the config_schema is the same
                plugin = plugin_objects[0]
                plugin_type = plugin.plugin_manifest.plugin_type
                schemas.setdefault(plugin_type, {})
                schemas[plugin_type][plugin.plugin_manifest.name] = plugin.config_schema
            except IndexError:
                pass

        return schemas

    def _get_all_plugins(self) -> List[Mapping[OperatingSystem, AgentPlugin]]:
        plugins = []

        plugin_file_names = self._plugin_file_repository.get_all_file_names()
        for plugin_file_name in plugin_file_names:
            plugin_name, plugin_type = plugin_file_name.split(".")[0].split("-")

            try:
                agent_plugin_type = AgentPluginType[plugin_type.upper()]
                plugin = self._load_plugin_from_file(agent_plugin_type, plugin_name)
                plugins.append(plugin)
            except KeyError as err:
                raise RetrievalError(
                    f"Error retrieving plugin {plugin_name} of "
                    f"type {plugin_type.upper()}: {err}"
                )

        return plugins

    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        manifests: Dict[AgentPluginType, Dict[str, AgentPluginManifest]] = {}
        for parsed_plugin in self._get_all_plugins():
            plugin_objects = list(parsed_plugin.values())
            try:
                # doesn't matter which OS's plugin this is since the manifest is the same
                plugin = plugin_objects[0]
                plugin_type = plugin.plugin_manifest.plugin_type
                manifests.setdefault(plugin_type, {})
                manifests[plugin_type][plugin.plugin_manifest.name] = plugin.plugin_manifest
            except IndexError:
                pass

        return manifests

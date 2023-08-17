import logging
from typing import Any, Dict, Generator, List, Mapping

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories import IFileRepository, RetrievalError

from .i_agent_plugin_repository import IAgentPluginRepository
from .plugin_archive_parser import parse_plugin

logger = logging.getLogger(__name__)


def _deduplicate_os_specific_plugins(
    plugins: List[Mapping[OperatingSystem, AgentPlugin]]
) -> Generator[AgentPlugin, None, None]:
    """
    Given OS-specific plugins, select only one plugin object per name

    Information like manifests and config schemas are OS-independent. This function takes
    OS-specific plugins and selects only one plugin object per name. The selected plugins may
    support any OS.
    """
    for plugin in plugins:
        yield list(plugin.values())[0]


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
        for plugin in _deduplicate_os_specific_plugins(self._get_all_plugins()):
            plugin_type = plugin.plugin_manifest.plugin_type
            schemas.setdefault(plugin_type, {})
            schemas[plugin_type][plugin.plugin_manifest.name] = plugin.config_schema

        return schemas

    def _get_all_plugins(self) -> List[Mapping[OperatingSystem, AgentPlugin]]:
        plugins = []

        plugin_file_names = self._plugin_file_repository.get_all_file_names()
        for plugin_file_name in plugin_file_names:
            plugins.append(self._load_plugin_from_file_name(plugin_file_name))

        return plugins

    def _load_plugin_from_file_name(
        self, plugin_file_name: str
    ) -> Mapping[OperatingSystem, AgentPlugin]:
        plugin_name, plugin_type = plugin_file_name.split(".")[0].split("-")

        try:
            agent_plugin_type = AgentPluginType[plugin_type.upper()]
        except KeyError as err:
            raise RetrievalError(
                f"Error retrieving plugin {plugin_name} of type {plugin_type.upper()}: {err}"
            )

        return self._load_plugin_from_file(agent_plugin_type, plugin_name)

    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        manifests: Dict[AgentPluginType, Dict[str, AgentPluginManifest]] = {}
        for plugin in _deduplicate_os_specific_plugins(self._get_all_plugins()):
            plugin_type = plugin.plugin_manifest.plugin_type
            manifests.setdefault(plugin_type, {})
            manifests[plugin_type][plugin.plugin_manifest.name] = plugin.plugin_manifest

        return manifests

    def store_agent_plugin(self, operating_system: OperatingSystem, agent_plugin: AgentPlugin):
        # TODO: Actually implement it
        logger.debug(
            f"The {agent_plugin.plugin_manifest.name} has been stored for "
            f"operaint system: {operating_system}"
        )

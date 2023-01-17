from typing import Sequence, Tuple

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginType

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

    def get_plugin(self, plugin_type: AgentPluginType, name: str) -> AgentPlugin:
        plugin_file_name = f"{name}-{plugin_type.value.lower()}.tar"

        try:
            with self._plugin_file_repository.open_file(plugin_file_name) as f:
                return parse_plugin(f)
        except ValueError as err:
            raise RetrievalError(f"Error retrieving the agent plugin {plugin_file_name}: {err}")

    def get_plugin_for_os(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        plugin = self.get_plugin(plugin_type, name)

        if host_operating_system in plugin.host_operating_systems:
            # TODO: Return the plugin with only the operating system specific dependencies
            return plugin
        else:
            raise RetrievalError(
                f"Error retrieving the agent plugin {name} of type {plugin_type} "
                f"for OS {host_operating_system}"
            )

    def get_plugin_catalog(self) -> Sequence[Tuple[AgentPluginType, str, Tuple[OperatingSystem]]]:
        plugin_catalog = []

        plugin_file_names = self._plugin_file_repository.get_all_file_names()
        for plugin_file_name in plugin_file_names:
            plugin_name, plugin_type = plugin_file_name.split(".")[0].split("-")

            try:
                agent_plugin_type = AgentPluginType[plugin_type.upper()]
                plugin = self.get_plugin(agent_plugin_type, plugin_name)
                operating_systems = plugin.host_operating_systems
                plugin_catalog.append(
                    (AgentPluginType[plugin_type.upper()], plugin_name, operating_systems)
                )
            except KeyError as err:
                raise RetrievalError(
                    f"Error retrieving plugin catalog for plugin {plugin_name} of "
                    f"type {plugin_type.upper()}: {err}"
                )

        return plugin_catalog

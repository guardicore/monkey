from typing import Sequence, Tuple

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

    def get_plugin_catalog(self) -> Sequence[Tuple[AgentPluginType, str]]:
        plugin_catalog = []

        plugin_file_names = self._plugin_file_repository.get_all_file_names()
        for plugin_file_name in plugin_file_names:
            plugin_name, plugin_type = plugin_file_name.split(".")[0].split("-")
            try:
                plugin_catalog.append((AgentPluginType[plugin_type.upper()], plugin_name))
            except KeyError as err:
                raise RetrievalError(
                    f"Error retrieving plugin catalog for plugin {plugin_name} of "
                    f"type {plugin_type.upper()}: {err}"
                )

        return plugin_catalog

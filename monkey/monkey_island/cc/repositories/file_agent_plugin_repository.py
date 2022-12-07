from common.agent_plugins import AgentPlugin, AgentPluginType

from . import IAgentPluginRepository, IFileRepository, RetrievalError
from .plugin_archive_parser import parse_plugin


class FileAgentPluginRepository(IAgentPluginRepository):
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository

    def get_plugin(self, name: str, plugin_type: AgentPluginType) -> AgentPlugin:
        plugin_file_name = f"{name}-{plugin_type.value.lower()}.tar"

        try:
            with self._file_repository.open_file(plugin_file_name) as f:
                return parse_plugin(f)
        except Exception as err:
            raise RetrievalError(f"Error retrieving the agent plugin {plugin_file_name}: {err}")

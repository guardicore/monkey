import io
from threading import Lock
from typing import Any, Dict

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType

from . import IAgentPluginService
from .i_agent_plugin_repository import IAgentPluginRepository
from .plugin_archive_parser import parse_plugin


class AgentPluginService(IAgentPluginService):
    """
    A service for retrieving and manipulating Agent plugins
    """

    def __init__(
        self,
        agent_plugin_repository: IAgentPluginRepository,
    ):
        self._agent_plugin_repository = agent_plugin_repository
        self._lock = Lock()

    def get_plugin(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        return self._agent_plugin_repository.get_plugin(host_operating_system, plugin_type, name)

    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        return self._agent_plugin_repository.get_all_plugin_configuration_schemas()

    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        return self._agent_plugin_repository.get_all_plugin_manifests()

    def install_agent_plugin_archive(self, agent_plugin_archive: bytes):
        with self._lock:
            os_agent_plugins = parse_plugin(io.BytesIO(agent_plugin_archive))

            plugin = next(iter(os_agent_plugins.values()))
            self._agent_plugin_repository.remove_agent_plugin(
                operating_system=None,
                agent_plugin_type=plugin.plugin_manifest.plugin_type,
                agent_plugin_name=plugin.plugin_manifest.name,
            )

            for operating_system, agent_plugin in os_agent_plugins.items():
                self._agent_plugin_repository.store_agent_plugin(
                    operating_system=operating_system, agent_plugin=agent_plugin
                )

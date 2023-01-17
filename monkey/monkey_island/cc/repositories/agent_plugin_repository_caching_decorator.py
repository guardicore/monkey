from functools import lru_cache
from typing import Any, Dict

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType

from . import IAgentPluginRepository


class AgentPluginRepositoryCachingDecorator(IAgentPluginRepository):
    """
    An IAgentPluginRepository decorator that provides caching for other IAgentPluginRepositories
    """

    def __init__(self, agent_plugin_repository: IAgentPluginRepository):
        self._agent_plugin_repository = agent_plugin_repository

    @lru_cache()
    def get_plugin(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        return self._agent_plugin_repository.get_plugin(host_operating_system, plugin_type, name)

    @lru_cache()
    def get_all_plugin_config_schemas(self) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        return self._agent_plugin_repository.get_all_plugin_config_schemas()

    @lru_cache()
    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        return self._agent_plugin_repository.get_all_plugin_manifests()

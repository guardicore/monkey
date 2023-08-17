from functools import lru_cache
from typing import Any, Dict, Optional

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType

from .i_agent_plugin_repository import IAgentPluginRepository


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
    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        return self._agent_plugin_repository.get_all_plugin_configuration_schemas()

    @lru_cache()
    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        return self._agent_plugin_repository.get_all_plugin_manifests()

    def store_agent_plugin(self, operating_system: OperatingSystem, agent_plugin: AgentPlugin):
        return self._agent_plugin_repository.store_agent_plugin(operating_system, agent_plugin)

    def remove_agent_plugin(
        self,
        operating_system: Optional[OperatingSystem],
        agent_plugin_name: str,
        agent_plugin_type: AgentPluginType,
    ):
        return self._agent_plugin_repository.remove_agent_plugin(
            operating_system, agent_plugin_name, agent_plugin_type
        )

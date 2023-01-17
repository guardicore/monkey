from functools import lru_cache
from typing import Any, Dict

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginType

from . import IAgentPluginRepository


class AgentPluginRepositoryCachingDecorator(IAgentPluginRepository):
    """
    An IAgentPluginRepository decorator that provides caching for other IAgentPluginRepositories
    """

    def __init__(self, agent_plugin_repository: IAgentPluginRepository):
        self._agent_plugin_repository = agent_plugin_repository

    @lru_cache()
    def get_plugin(self, plugin_type: AgentPluginType, name: str) -> AgentPlugin:
        return self._agent_plugin_repository.get_plugin(plugin_type, name)

    @lru_cache()
    def get_plugin_for_os(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        return self._agent_plugin_repository.get_plugin_for_os(
            host_operating_system, plugin_type, name
        )

    @lru_cache()
    def get_all_plugin_config_schemas(self) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        return self._agent_plugin_repository.get_all_plugin_config_schemas()

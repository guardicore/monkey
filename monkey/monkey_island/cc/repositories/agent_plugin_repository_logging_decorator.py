import logging
from typing import Any, Dict

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginType

from . import IAgentPluginRepository

logger = logging.getLogger(__name__)


class AgentPluginRepositoryLoggingDecorator(IAgentPluginRepository):
    """
    An IAgentPluginRepository decorator that provides debug logging for other
    IAgentPluginRepositories
    """

    def __init__(self, agent_plugin_repository: IAgentPluginRepository):
        self._agent_plugin_repository = agent_plugin_repository

    def get_plugin(self, plugin_type: AgentPluginType, name: str) -> AgentPlugin:
        logger.debug(f"Retrieving plugin {name} of type {plugin_type}")
        return self._agent_plugin_repository.get_plugin(plugin_type, name)

    def get_plugin_for_os(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        logger.debug(
            f"Retrieving plugin {name} of type {plugin_type} for os {host_operating_system}"
        )
        return self._agent_plugin_repository.get_plugin_for_os(
            host_operating_system, plugin_type, name
        )

    def get_all_plugin_config_schemas(self) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        logger.debug("Retrieving plugin config schemas")
        return self._agent_plugin_repository.get_all_plugin_config_schemas()

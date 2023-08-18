import logging
from typing import Any, Dict, Optional

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType

from .i_agent_plugin_repository import IAgentPluginRepository

logger = logging.getLogger(__name__)


class AgentPluginRepositoryLoggingDecorator(IAgentPluginRepository):
    """
    An IAgentPluginRepository decorator that provides debug logging for other
    IAgentPluginRepositories
    """

    def __init__(self, agent_plugin_repository: IAgentPluginRepository):
        self._agent_plugin_repository = agent_plugin_repository

    def get_plugin(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        logger.debug(f"Retrieving plugin {name} of type {plugin_type}")
        return self._agent_plugin_repository.get_plugin(host_operating_system, plugin_type, name)

    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        logger.debug("Retrieving plugin configuration schemas")
        return self._agent_plugin_repository.get_all_plugin_configuration_schemas()

    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        logger.debug("Retrieving plugin manifests")
        return self._agent_plugin_repository.get_all_plugin_manifests()

    def store_agent_plugin(self, operating_system: OperatingSystem, agent_plugin: AgentPlugin):
        logger.debug(
            f"Storing {agent_plugin.plugin_manifest.name} "
            f"for operating system: {operating_system}"
        )
        return self._agent_plugin_repository.store_agent_plugin(operating_system, agent_plugin)

    def remove_agent_plugin(
        self,
        operating_system: Optional[OperatingSystem],
        agent_plugin_type: AgentPluginType,
        agent_plugin_name: str,
    ):
        logger.debug(
            f"Removing {agent_plugin_name} of type {agent_plugin_type} "
            f"for operating system: {operating_system}"
        )
        return self._agent_plugin_repository.remove_agent_plugin(
            operating_system, agent_plugin_type, agent_plugin_name
        )

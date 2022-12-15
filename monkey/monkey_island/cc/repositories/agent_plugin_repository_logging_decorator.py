import logging
from typing import Sequence, Tuple

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

    def get_plugin_catalog(self) -> Sequence[Tuple[AgentPluginType, str]]:
        logger.debug("Retrieving plugin catalog")
        return self._agent_plugin_repository.get_plugin_catalog()

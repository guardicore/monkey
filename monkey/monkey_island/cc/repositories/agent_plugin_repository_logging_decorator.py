import logging

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

    def get_plugin(self, name: str, plugin_type: AgentPluginType) -> AgentPlugin:
        logger.debug(f"Retrieving plugin {name} of type {plugin_type}")
        return self._agent_plugin_repository.get_plugin(name, plugin_type)

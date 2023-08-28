from common import DIContainer
from monkey_island.cc.deployment import Deployment

from .agent_plugin_repository_logging_decorator import AgentPluginRepositoryLoggingDecorator
from .agent_plugin_service import AgentPluginService
from .i_agent_plugin_repository import IAgentPluginRepository
from .i_agent_plugin_service import IAgentPluginService
from .mongo_agent_plugin_repository import MongoAgentPluginRepository


def build(container: DIContainer, deployment: Deployment) -> IAgentPluginService:
    undecorated_agent_plugin_repository = container.resolve(MongoAgentPluginRepository)
    agent_plugin_repository = _decorate_agent_plugin_repository(undecorated_agent_plugin_repository)
    agent_plugin_service = AgentPluginService(agent_plugin_repository, deployment)
    container.register_instance(IAgentPluginService, agent_plugin_service)

    return agent_plugin_service


def _decorate_agent_plugin_repository(
    plugin_repository: IAgentPluginRepository,
) -> IAgentPluginRepository:
    return AgentPluginRepositoryLoggingDecorator(plugin_repository)

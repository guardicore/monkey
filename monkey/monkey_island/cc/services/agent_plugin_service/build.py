from common import DIContainer

from .agent_plugin_repository_caching_decorator import AgentPluginRepositoryCachingDecorator
from .agent_plugin_repository_logging_decorator import AgentPluginRepositoryLoggingDecorator
from .agent_plugin_service import AgentPluginService
from .file_agent_plugin_repository import FileAgentPluginRepository
from .i_agent_plugin_repository import IAgentPluginRepository
from .i_agent_plugin_service import IAgentPluginService


def build(container: DIContainer) -> IAgentPluginService:
    undecorated_agent_plugin_repository = container.resolve(FileAgentPluginRepository)
    agent_plugin_repository = _decorate_agent_plugin_repository(undecorated_agent_plugin_repository)
    agent_plugin_service = AgentPluginService(agent_plugin_repository)
    container.register_instance(IAgentPluginService, agent_plugin_service)

    return agent_plugin_service


def _decorate_agent_plugin_repository(
    plugin_repository: IAgentPluginRepository,
) -> IAgentPluginRepository:
    return AgentPluginRepositoryLoggingDecorator(
        AgentPluginRepositoryCachingDecorator(plugin_repository)
    )

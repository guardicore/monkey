from common import DIContainer
from monkey_island.cc.event_queue import IIslandEventQueue, IslandEventTopic

from . import IAgentConfigurationService
from .agent_configuration_schema_compiler import AgentConfigurationSchemaCompiler
from .agent_configuration_service import AgentConfigurationService
from .agent_configuration_validation_decorator import AgentConfigurationValidationDecorator
from .event_handlers import reset_agent_configuration
from .file_agent_configuration_repository import FileAgentConfigurationRepository
from .i_agent_configuration_repository import IAgentConfigurationRepository


def build(container: DIContainer) -> IAgentConfigurationService:
    schema_compiler = container.resolve(AgentConfigurationSchemaCompiler)
    agent_configuration_repository = _build_file_agent_configuration_repository(
        container, schema_compiler
    )

    agent_configuration_service = AgentConfigurationService(
        agent_configuration_repository, schema_compiler
    )
    container.register_instance(IAgentConfigurationService, agent_configuration_service)

    _register_event_handlers(container)

    return agent_configuration_service


def _build_file_agent_configuration_repository(
    container: DIContainer, schema_compiler: AgentConfigurationSchemaCompiler
) -> IAgentConfigurationRepository:
    file_agent_configuration_repository = container.resolve(FileAgentConfigurationRepository)
    return _decorate_agent_configuration_repository(
        file_agent_configuration_repository, schema_compiler
    )


def _decorate_agent_configuration_repository(
    agent_configuration_repository: IAgentConfigurationRepository,
    schema_compiler: AgentConfigurationSchemaCompiler,
) -> IAgentConfigurationRepository:
    return AgentConfigurationValidationDecorator(agent_configuration_repository, schema_compiler)


def _register_event_handlers(container: DIContainer) -> None:
    island_event_queue = container.resolve(IIslandEventQueue)

    island_event_queue.subscribe(
        IslandEventTopic.RESET_AGENT_CONFIGURATION,
        container.resolve(reset_agent_configuration),
    )

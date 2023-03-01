from common import DIContainer
from monkey_island.cc.repositories import (
    AgentConfigurationValidationDecorator,
    FileAgentConfigurationRepository,
    IAgentConfigurationRepository,
)
from monkey_island.cc.repositories.utils import AgentConfigurationSchemaCompiler

from . import IAgentConfigurationService
from .agent_configuration_service import AgentConfigurationService


def build(container: DIContainer) -> IAgentConfigurationService:
    schema_compiler = container.resolve(AgentConfigurationSchemaCompiler)
    agent_configuration_repository = _build_file_agent_configuration_repository(
        container, schema_compiler
    )

    return AgentConfigurationService(agent_configuration_repository, schema_compiler)


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

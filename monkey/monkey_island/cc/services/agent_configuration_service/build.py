from common import DIContainer
from monkey_island.cc.repositories import FileAgentConfigurationRepository
from monkey_island.cc.repositories.utils import AgentConfigurationSchemaCompiler

from . import IAgentConfigurationService
from .agent_configuration_service import AgentConfigurationService


def build(container: DIContainer) -> IAgentConfigurationService:
    agent_configuration_repository = container.resolve(FileAgentConfigurationRepository)
    schema_compiler = container.resolve(AgentConfigurationSchemaCompiler)

    return AgentConfigurationService(agent_configuration_repository, schema_compiler)

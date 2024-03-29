from common.agent_configuration import AgentConfiguration

from . import IAgentConfigurationService
from .agent_configuration_schema_compiler import AgentConfigurationSchemaCompiler
from .i_agent_configuration_repository import IAgentConfigurationRepository


class AgentConfigurationService(IAgentConfigurationService):
    """
    A service for storing and retrieving the agent configuration.
    """

    def __init__(
        self,
        agent_configuration_repository: IAgentConfigurationRepository,
        schema_compiler: AgentConfigurationSchemaCompiler,
    ):
        self._repository = agent_configuration_repository
        self._schema_compiler = schema_compiler

    def get_schema(self):
        return self._schema_compiler.get_schema()

    def get_configuration(self) -> AgentConfiguration:
        return self._repository.get_configuration()

    def update_configuration(self, agent_configuration: AgentConfiguration):
        return self._repository.update_configuration(agent_configuration)

    def reset_to_default(self):
        return self._repository.reset_to_default()

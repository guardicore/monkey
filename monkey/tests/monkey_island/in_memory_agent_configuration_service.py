from common.agent_configuration import AgentConfiguration
from monkey_island.cc.services import IAgentConfigurationService

from . import InMemoryAgentConfigurationRepository


class InMemoryAgentConfigurationService(IAgentConfigurationService):
    def __init__(self):
        self._repository = InMemoryAgentConfigurationRepository()

    def get_schema(self):
        raise NotImplementedError()

    def get_configuration(self) -> AgentConfiguration:
        return self._repository.get_configuration()

    def update_configuration(self, agent_configuration: AgentConfiguration):
        return self._repository.update_configuration(agent_configuration)

    def reset_to_default(self):
        return self._repository.reset_to_default()

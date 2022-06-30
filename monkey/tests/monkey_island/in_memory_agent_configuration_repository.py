from tests.common.example_agent_configuration import AGENT_CONFIGURATION

from common.configuration.agent_configuration import AgentConfiguration
from monkey_island.cc.repository import IAgentConfigurationRepository


class InMemoryAgentConfigurationRepository(IAgentConfigurationRepository):
    def __init__(self):
        self._default_configuration = AgentConfiguration.from_mapping(AGENT_CONFIGURATION)
        self._configuration = self._default_configuration

    def get_configuration(self):
        return self._configuration

    def store_configuration(self, agent_configuration):
        self._configuration = agent_configuration

    def reset_to_default(self):
        self._configuration = self._default_configuration

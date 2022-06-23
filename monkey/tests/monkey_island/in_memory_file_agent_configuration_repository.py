from tests.common.example_agent_configuration import AGENT_CONFIGURATION

from common.configuration.agent_configuration import AgentConfigurationSchema
from monkey_island.cc.repository import IAgentConfigurationRepository


class InMemoryFileAgentConfigurationRepository(IAgentConfigurationRepository):
    def __init__(self):
        self._configuration = AgentConfigurationSchema().load(AGENT_CONFIGURATION)

    def get_configuration(self):
        return self._configuration

    def store_configuration(self, agent_configuration):
        self._configuration = agent_configuration

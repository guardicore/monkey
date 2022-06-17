from tests.common.example_agent_configuration import AGENT_CONFIGURATION
from tests.monkey_island import SingleFileRepository

from common.configuration import AgentConfigurationSchema
from monkey_island.cc.repository import FileAgentConfigurationRepository


def test_store_agent_config():
    repository = FileAgentConfigurationRepository(SingleFileRepository())
    schema = AgentConfigurationSchema()
    agent_configuration = schema.load(AGENT_CONFIGURATION)

    repository.store_configuration(agent_configuration)
    retrieved_agent_configuration = repository.get_configuration()

    assert retrieved_agent_configuration == agent_configuration

import pytest
from tests.common.example_agent_configuration import AGENT_CONFIGURATION
from tests.monkey_island import OpenErrorFileRepository, SingleFileRepository

from common.configuration import DEFAULT_AGENT_CONFIGURATION, AgentConfigurationSchema
from monkey_island.cc.repository import FileAgentConfigurationRepository, RetrievalError


def test_store_agent_config():
    repository = FileAgentConfigurationRepository(SingleFileRepository())
    schema = AgentConfigurationSchema()
    agent_configuration = schema.load(AGENT_CONFIGURATION)

    repository.store_configuration(agent_configuration)
    retrieved_agent_configuration = repository.get_configuration()

    assert retrieved_agent_configuration == agent_configuration


def test_get_default_agent_config():
    repository = FileAgentConfigurationRepository(SingleFileRepository())
    schema = AgentConfigurationSchema()
    default_agent_configuration = schema.loads(DEFAULT_AGENT_CONFIGURATION)

    retrieved_agent_configuration = repository.get_configuration()

    assert retrieved_agent_configuration == default_agent_configuration


def test_get_agent_config_retrieval_error():
    repository = FileAgentConfigurationRepository(OpenErrorFileRepository())

    with pytest.raises(RetrievalError):
        repository.get_configuration()

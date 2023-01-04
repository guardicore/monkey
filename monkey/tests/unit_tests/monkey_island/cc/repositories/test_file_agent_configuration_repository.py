import pytest
from tests.common.example_agent_configuration import AGENT_CONFIGURATION
from tests.monkey_island import OpenErrorFileRepository, SingleFileRepository

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.repositories import FileAgentConfigurationRepository, RetrievalError


@pytest.fixture
def repository(default_agent_configuration):
    return FileAgentConfigurationRepository(default_agent_configuration, SingleFileRepository())


def test_store_agent_config(repository):
    agent_configuration = AgentConfiguration(**AGENT_CONFIGURATION)

    repository.update_configuration(agent_configuration)
    retrieved_agent_configuration = repository.get_configuration()

    assert retrieved_agent_configuration == agent_configuration


def test_get_default_agent_config(repository, default_agent_configuration):
    retrieved_agent_configuration = repository.get_configuration()

    assert retrieved_agent_configuration == default_agent_configuration


def test_get_agent_config_retrieval_error(default_agent_configuration):
    repository = FileAgentConfigurationRepository(
        default_agent_configuration, OpenErrorFileRepository()
    )

    with pytest.raises(RetrievalError):
        repository.get_configuration()


def test_reset_to_default(repository, default_agent_configuration):
    agent_configuration = AgentConfiguration(**AGENT_CONFIGURATION)

    repository.update_configuration(agent_configuration)
    repository.reset_to_default()
    retrieved_agent_configuration = repository.get_configuration()

    assert retrieved_agent_configuration == default_agent_configuration

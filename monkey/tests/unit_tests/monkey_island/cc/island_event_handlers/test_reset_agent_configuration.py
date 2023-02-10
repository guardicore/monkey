import pytest
from tests.monkey_island import InMemoryAgentConfigurationRepository

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.island_event_handlers import reset_agent_configuration
from monkey_island.cc.repositories import IAgentConfigurationRepository


@pytest.fixture
def agent_configuration(default_agent_configuration: AgentConfiguration) -> AgentConfiguration:
    return default_agent_configuration.copy()


@pytest.fixture
def agent_configuration_repository(
    agent_configuration: AgentConfiguration,
) -> IAgentConfigurationRepository:
    agent_configuration_repository = InMemoryAgentConfigurationRepository()
    agent_configuration_repository.update_configuration(agent_configuration)

    return agent_configuration_repository


@pytest.fixture
def callable_reset_agent_configuration(
    agent_configuration_repository: IAgentConfigurationRepository,
) -> reset_agent_configuration:
    return reset_agent_configuration(agent_configuration_repository)


def test_reset_configuration__agent_configuration_changed(
    callable_reset_agent_configuration, agent_configuration_repository, agent_configuration
):
    agent_configuration.keep_tunnel_open_time = 99
    callable_reset_agent_configuration()

    assert agent_configuration_repository.get_configuration() != agent_configuration

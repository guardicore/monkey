import pytest
from tests.monkey_island import InMemoryAgentConfigurationService

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.island_event_handlers import reset_agent_configuration
from monkey_island.cc.services import IAgentConfigurationService


@pytest.fixture
def agent_configuration(default_agent_configuration: AgentConfiguration) -> AgentConfiguration:
    return default_agent_configuration


@pytest.fixture
def agent_configuration_service(
    agent_configuration: AgentConfiguration,
) -> IAgentConfigurationService:
    agent_configuration_service = InMemoryAgentConfigurationService()
    agent_configuration_service.update_configuration(agent_configuration)

    return agent_configuration_service


@pytest.fixture
def callable_reset_agent_configuration(
    agent_configuration_service: IAgentConfigurationService,
) -> reset_agent_configuration:
    return reset_agent_configuration(agent_configuration_service)


def test_reset_configuration__agent_configuration_changed(
    callable_reset_agent_configuration, agent_configuration_service, agent_configuration
):
    agent_configuration.keep_tunnel_open_time = 99
    callable_reset_agent_configuration()

    assert agent_configuration_service.get_configuration() != agent_configuration

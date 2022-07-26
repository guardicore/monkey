import pytest
from tests.monkey_island import InMemoryAgentConfigurationRepository, InMemorySimulationRepository

from common.agent_configuration import (
    DEFAULT_AGENT_CONFIGURATION,
    DEFAULT_RANSOMWARE_AGENT_CONFIGURATION,
)
from monkey_island.cc.models import IslandMode
from monkey_island.cc.services import IslandModeService


@pytest.fixture
def agent_configuration_repository():
    return InMemoryAgentConfigurationRepository()


@pytest.fixture
def island_mode_service(agent_configuration_repository):
    return IslandModeService(
        agent_configuration_repository,
        InMemorySimulationRepository(),
        DEFAULT_AGENT_CONFIGURATION,
        DEFAULT_RANSOMWARE_AGENT_CONFIGURATION,
    )


@pytest.mark.parametrize("mode", list(IslandMode))
def test_set_mode(island_mode_service, mode):
    island_mode_service.set_mode(mode)
    assert island_mode_service.get_mode() == mode


@pytest.mark.parametrize(
    "mode, expected_config",
    [
        (IslandMode.UNSET, DEFAULT_AGENT_CONFIGURATION),
        (IslandMode.ADVANCED, DEFAULT_AGENT_CONFIGURATION),
        (IslandMode.RANSOMWARE, DEFAULT_RANSOMWARE_AGENT_CONFIGURATION),
    ],
)
def test_set_mode_sets_config(
    island_mode_service, agent_configuration_repository, mode, expected_config
):
    island_mode_service.set_mode(mode)
    assert agent_configuration_repository.get_configuration() == expected_config

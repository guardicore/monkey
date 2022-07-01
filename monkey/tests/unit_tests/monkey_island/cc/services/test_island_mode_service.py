import pytest
from tests.monkey_island import InMemorySimulationRepository

from monkey_island.cc.services import IslandModeService
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum


@pytest.fixture
def island_mode_service():
    return IslandModeService(InMemorySimulationRepository())


@pytest.mark.parametrize("mode", list(IslandModeEnum))
def test_set_mode(island_mode_service, mode):
    island_mode_service.set_mode(mode)
    assert island_mode_service.get_mode() == mode

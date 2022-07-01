import pytest
from tests.monkey_island import OpenErrorFileRepository, SingleFileRepository

from monkey_island.cc.models import IslandModeEnum, Simulation
from monkey_island.cc.repository import FileSimulationRepository, RetrievalError


@pytest.fixture
def simulation_repository():
    return FileSimulationRepository(SingleFileRepository())


@pytest.mark.parametrize("mode", list(IslandModeEnum))
def test_save_simulation(simulation_repository, mode):
    simulation = Simulation(mode)
    simulation_repository.save_simulation(simulation)

    assert simulation_repository.get_simulation() == simulation


def test_get_default_simulation(simulation_repository):
    default_simulation = Simulation()

    assert simulation_repository.get_simulation() == default_simulation


def test_set_mode(simulation_repository):
    simulation_repository.set_mode(IslandModeEnum.ADVANCED)

    assert simulation_repository.get_mode() == IslandModeEnum.ADVANCED


def test_get_mode_default(simulation_repository):
    assert simulation_repository.get_mode() == IslandModeEnum.UNSET


def test_get_simulation_retrieval_error():
    simulation_repository = FileSimulationRepository(OpenErrorFileRepository())

    with pytest.raises(RetrievalError):
        simulation_repository.get_simulation()


def test_get_mode_retrieval_error():
    simulation_repository = FileSimulationRepository(OpenErrorFileRepository())

    with pytest.raises(RetrievalError):
        simulation_repository.get_mode()

import pytest
from tests.monkey_island import OpenErrorFileRepository, SingleFileRepository

from monkey_island.cc.models import IslandMode, Simulation
from monkey_island.cc.repositories import FileSimulationRepository, RetrievalError


@pytest.fixture
def simulation_repository():
    return FileSimulationRepository(SingleFileRepository())


@pytest.mark.parametrize("mode", list(IslandMode))
def test_save_simulation(simulation_repository, mode):
    simulation = Simulation(mode=mode)
    simulation_repository.save_simulation(simulation)

    assert simulation_repository.get_simulation() == simulation


def test_get_default_simulation(simulation_repository):
    default_simulation = Simulation()

    assert simulation_repository.get_simulation() == default_simulation


def test_set_mode(simulation_repository):
    simulation_repository.set_mode(IslandMode.ADVANCED)

    assert simulation_repository.get_mode() == IslandMode.ADVANCED


def test_get_mode_default(simulation_repository):
    assert simulation_repository.get_mode() == IslandMode.UNSET


def test_get_simulation_retrieval_error():
    simulation_repository = FileSimulationRepository(OpenErrorFileRepository())

    with pytest.raises(RetrievalError):
        simulation_repository.get_simulation()


def test_get_mode_retrieval_error():
    simulation_repository = FileSimulationRepository(OpenErrorFileRepository())

    with pytest.raises(RetrievalError):
        simulation_repository.get_mode()

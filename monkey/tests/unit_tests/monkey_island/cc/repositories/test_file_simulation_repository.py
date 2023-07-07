import datetime

import pytest
from tests.monkey_island import OpenErrorFileRepository, SingleFileRepository

from monkey_island.cc.models import Simulation
from monkey_island.cc.repositories import FileSimulationRepository, RetrievalError


@pytest.fixture
def simulation_repository():
    return FileSimulationRepository(SingleFileRepository())


def test_save_simulation(simulation_repository):
    simulation = Simulation(terminate_signal_time=datetime.datetime.now())
    simulation_repository.save_simulation(simulation)

    assert simulation_repository.get_simulation() == simulation


def test_get_default_simulation(simulation_repository):
    default_simulation = Simulation()

    assert simulation_repository.get_simulation() == default_simulation


def test_get_simulation_retrieval_error():
    simulation_repository = FileSimulationRepository(OpenErrorFileRepository())

    with pytest.raises(RetrievalError):
        simulation_repository.get_simulation()

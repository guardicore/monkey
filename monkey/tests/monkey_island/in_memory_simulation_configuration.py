from monkey_island.cc.models import Simulation
from monkey_island.cc.repositories import ISimulationRepository


class InMemorySimulationRepository(ISimulationRepository):
    def __init__(self):
        self._simulation = Simulation()

    def get_simulation(self) -> Simulation:
        return self._simulation

    def save_simulation(self, simulation: Simulation):
        self._simulation = simulation

from monkey_island.cc.models import IslandMode, Simulation
from monkey_island.cc.repositories import ISimulationRepository


class InMemorySimulationRepository(ISimulationRepository):
    def __init__(self):
        self._simulation = Simulation()

    def get_simulation(self) -> Simulation:
        return self._simulation

    def save_simulation(self, simulation: Simulation):
        self._simulation = simulation

    def get_mode(self) -> IslandMode:
        return self._simulation.mode

    def set_mode(self, mode: IslandMode):
        self._simulation = Simulation(mode=mode)

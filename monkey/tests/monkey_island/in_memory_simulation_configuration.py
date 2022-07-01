import dataclasses

from monkey_island.cc.models import IslandModeEnum, Simulation
from monkey_island.cc.repository import ISimulationRepository


class InMemorySimulationRepository(ISimulationRepository):
    def __init__(self):
        self._simulation = Simulation()

    def get_simulation(self) -> Simulation:
        return self._simulation

    def save_simulation(self, simulation: Simulation):
        self._simulation = simulation

    def get_mode(self) -> IslandModeEnum:
        return self._simulation.mode

    def set_mode(self, mode: IslandModeEnum):
        self._simulation = dataclasses.replace(self._simulation, mode=mode)

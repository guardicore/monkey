from abc import ABC

from monkey_island.cc.models import Simulation


class ISimulationRepository(ABC):
    def save_simulation(self, simulation: Simulation):
        pass

    def get_simulation(self):
        pass

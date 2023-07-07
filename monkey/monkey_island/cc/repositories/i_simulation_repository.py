from abc import ABC, abstractmethod

from monkey_island.cc.models import Simulation


class ISimulationRepository(ABC):
    @abstractmethod
    def get_simulation(self) -> Simulation:
        """
        Get the simulation state

        :raises RetrievalError: If the simulation state could not be retrieved
        """

        pass

    @abstractmethod
    def save_simulation(self, simulation: Simulation):
        """
        Save the simulation state

        :param simulation: The simulation state
        :raises StorageError: If the simulation states could not be saved
        """

        pass

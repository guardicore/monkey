from abc import ABC, abstractmethod

from monkey_island.cc.models import IslandMode, Simulation


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

    @abstractmethod
    def get_mode(self) -> IslandMode:
        """
        Get's the island's current mode

        :return The island's current mode
        :raises RetrievalError: If the mode could not be retrieved
        """

        pass

    @abstractmethod
    def set_mode(self, mode: IslandMode):
        """
        Set the island's mode

        :param mode: The island's new mode
        :raises StorageError: If the mode could not be saved
        """

        pass

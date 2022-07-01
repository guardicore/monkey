from monkey_island.cc.repository import ISimulationRepository
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum


class IslandModeService:
    def __init__(self, simulation_repository: ISimulationRepository):
        self._simulation_repository = simulation_repository

    def get_mode(self):
        """
        Get's the island's current mode

        :return The island's current mode
        :raises RetrievalError: If the mode could not be retrieved
        """
        return self._simulation_repository.get_mode()

    def set_mode(self, mode: IslandModeEnum):
        """
        Set the island's mode

        :param mode: The island's new mode
        :raises StorageError: If the mode could not be saved
        """
        self._simulation_repository.set_mode(mode)

from abc import ABC, abstractmethod


class IIslandAPIClient(ABC):
    @abstractmethod
    def __init__(self, island_server: str):
        """
        Construct and API client and connect it to the island

        :param island_server: String representing the island ip address and port
        :raises IslandAPIError: If connection was unsuccessful
        """

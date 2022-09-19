from abc import ABC, abstractmethod


class IIslandAPIClient(ABC):
    """
    A client for the Island's API
    """

    @abstractmethod
    def __init__(self, island_server: str):
        """
        Construct and island API client and connect it to the island

        :param island_server: The socket address of the API
        :raises IslandAPIConnectionError: If a connection cannot be made to the island
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurred while attempting to connect to the
                                island
        """

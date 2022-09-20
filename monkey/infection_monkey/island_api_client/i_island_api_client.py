from abc import ABC, abstractmethod
from typing import Optional


class IIslandAPIClient(ABC):
    """
    A client for the Island's API
    """

    @abstractmethod
    def __init__(self, island_server: str):
        """
        Construct an island API client and connect it to the island

        :param island_server: The socket address of the API
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to connect to the
                                island
        """

    @abstractmethod
    def send_log(self, log_contents: str):
        """
        Send the contents of the agent's log to the island

        :param log_contents: The contents of the agent's log
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to send the
                                contents of the agent's log to the island
        """

    @abstractmethod
    def get_pba_file(self, filename: str) -> bytes:
        """
        Get a custom PBA file from the island

        :param filename: The name of the custom PBA file
        :return: The contents of the custom PBA file in bytes
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to retrieve the
                                custom PBA file
        """

    @abstractmethod
    def get_agent_binary(self, os_name: str) -> Optional[bytes]:
        """
        Get an agent binary for the given OS from the island

        :param os_name: The OS on which the agent binary will run
        :return: The agent binary file
        :raises IslandAPIConnectionError: If the client cannot successfully connect to the island
        :raises IslandAPIRequestError: If an error occurs while attempting to connect to the
                                       island due to an issue in the request sent from the client
        :raises IslandAPIRequestFailedError: If an error occurs while attempting to connect to the
                                             island due to an error on the server
        :raises IslandAPITimeoutError: If a timeout occurs while attempting to connect to the island
        :raises IslandAPIError: If an unexpected error occurs while attempting to retrieve the
                                agent binary
        """

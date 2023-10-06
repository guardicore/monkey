from abc import ABC, abstractmethod

from monkeytypes import SocketAddress

from . import IIslandAPIClient


class AbstractIslandAPIClientFactory(ABC):
    @abstractmethod
    def create_island_api_client(self, server: SocketAddress) -> IIslandAPIClient:
        """
        Create an IIslandAPIClient

        :param server: A SocketAddress for the server
        :return: A concrete instance of an IIslandAPIClient
        """

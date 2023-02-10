from abc import ABC, abstractmethod

from . import IIslandAPIClient


class AbstractIslandAPIClientFactory(ABC):
    @abstractmethod
    def create_island_api_client(self) -> IIslandAPIClient:
        """
        Create an IIslandAPIClient

        :return: A concrete instance of an IIslandAPIClient
        """

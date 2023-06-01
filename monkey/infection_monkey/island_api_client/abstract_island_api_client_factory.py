from abc import ABC, abstractmethod

from common.agent_event_serializers import AgentEventSerializerRegistry
from common.types import SocketAddress

from . import IIslandAPIClient


class AbstractIslandAPIClientFactory(ABC):
    @abstractmethod
    def create_island_api_client(
        self,
        server: SocketAddress,
        agent_event_serializer_registry: AgentEventSerializerRegistry,
    ) -> IIslandAPIClient:
        """
        Create an IIslandAPIClient

        :param server: A SocketAddress for the server
        :param agent_event_serializer_registry: An AgentEventSerializerRegistry
        :return: A concrete instance of an IIslandAPIClient
        """

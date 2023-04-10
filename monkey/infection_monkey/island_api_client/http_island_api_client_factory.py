from multiprocessing.managers import SyncManager

from common.agent_event_serializers import AgentEventSerializerRegistry
from common.types import AgentID, SocketAddress

from . import AbstractIslandAPIClientFactory, ConfigurationValidatorDecorator, IIslandAPIClient
from .http_client import HTTPClient


class HTTPIslandAPIClientFactory(AbstractIslandAPIClientFactory):
    def __init__(
        self,
        agent_event_serializer_registry: AgentEventSerializerRegistry,
        agent_id: AgentID,
        manager: SyncManager,
    ):
        self._agent_event_serializer_registry = agent_event_serializer_registry
        self._agent_id = agent_id
        self._manager = manager

    def create_island_api_client(self, server: SocketAddress) -> IIslandAPIClient:
        return ConfigurationValidatorDecorator(
            self._manager.HTTPIslandAPIClient(
                self._agent_event_serializer_registry,
                HTTPClient(f"https://{server}/api"),
                self._agent_id,
            )
        )

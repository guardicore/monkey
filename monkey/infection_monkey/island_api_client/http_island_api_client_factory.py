from monkeytypes import BasicLock

from common.agent_event_serializers import AgentEventSerializerRegistry
from common.types import AgentID, SocketAddress

from . import (
    AbstractIslandAPIClientFactory,
    ConfigurationValidatorDecorator,
    HTTPIslandAPIClient,
    IIslandAPIClient,
)
from .http_client import HTTPClient


class HTTPIslandAPIClientFactory(AbstractIslandAPIClientFactory):
    def __init__(
        self,
        agent_event_serializer_registry: AgentEventSerializerRegistry,
        agent_id: AgentID,
        lock: BasicLock,
    ):
        self._agent_event_serializer_registry = agent_event_serializer_registry
        self._agent_id = agent_id
        self._lock = lock

    def create_island_api_client(self, server: SocketAddress) -> IIslandAPIClient:
        return ConfigurationValidatorDecorator(
            HTTPIslandAPIClient(
                self._agent_event_serializer_registry,
                HTTPClient(f"https://{server}/api"),
                self._agent_id,
                self._lock,
            )
        )

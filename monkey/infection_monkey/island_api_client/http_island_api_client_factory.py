from common.agent_event_serializers import AgentEventSerializerRegistry

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
    ):
        self._agent_event_serializer_registry = agent_event_serializer_registry

    def create_island_api_client(self) -> IIslandAPIClient:
        return ConfigurationValidatorDecorator(
            HTTPIslandAPIClient(self._agent_event_serializer_registry, HTTPClient())
        )

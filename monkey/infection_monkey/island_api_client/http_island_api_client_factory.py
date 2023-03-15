from common.agent_event_serializers import AgentEventSerializerRegistry

from . import (
    AbstractIslandAPIClientFactory,
    ConfigurationValidatorDecorator,
    HTTPIslandAPIClient,
    IIslandAPIClient,
)


class HTTPIslandAPIClientFactory(AbstractIslandAPIClientFactory):
    def __init__(self, agent_event_serializer_registry: AgentEventSerializerRegistry, otp: str):
        self._agent_event_serializer_registry = agent_event_serializer_registry
        self._otp = otp

    def create_island_api_client(self) -> IIslandAPIClient:
        return ConfigurationValidatorDecorator(
            HTTPIslandAPIClient(self._agent_event_serializer_registry, self._otp)
        )

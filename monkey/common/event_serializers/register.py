from common.events import CredentialsStolenEvent

from . import AgentEventSerializerRegistry, PydanticEventSerializer


def register_common_agent_event_serializers(
    event_serializer_registry: AgentEventSerializerRegistry,
):
    event_serializer_registry[CredentialsStolenEvent] = PydanticEventSerializer(
        CredentialsStolenEvent
    )

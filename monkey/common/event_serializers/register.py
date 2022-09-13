from common.events import CredentialsStolenEvent

from . import EventSerializerRegistry, PydanticEventSerializer


def register_common_agent_event_serializers(event_serializer_registry: EventSerializerRegistry):
    event_serializer_registry[CredentialsStolenEvent] = PydanticEventSerializer(
        CredentialsStolenEvent
    )

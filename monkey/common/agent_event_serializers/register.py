from common.events import CredentialsStolenEvent

from . import AgentEventSerializerRegistry, PydanticAgentEventSerializer


def register_common_agent_event_serializers(
    event_serializer_registry: AgentEventSerializerRegistry,
):
    event_serializer_registry[CredentialsStolenEvent] = PydanticAgentEventSerializer(
        CredentialsStolenEvent
    )

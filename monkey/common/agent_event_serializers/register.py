from common.agent_events import (
    AgentShutdownEvent,
    CredentialsStolenEvent,
    ExploitationEvent,
    FileEncryptionEvent,
    HostnameDiscoveryEvent,
    OSDiscoveryEvent,
    PasswordRestorationEvent,
    PingScanEvent,
    PropagationEvent,
    TCPScanEvent,
)

from . import AgentEventSerializerRegistry, PydanticAgentEventSerializer


def register_common_agent_event_serializers(
    event_serializer_registry: AgentEventSerializerRegistry,
):
    event_serializer_registry[CredentialsStolenEvent] = PydanticAgentEventSerializer(
        CredentialsStolenEvent
    )
    event_serializer_registry[PingScanEvent] = PydanticAgentEventSerializer(PingScanEvent)
    event_serializer_registry[TCPScanEvent] = PydanticAgentEventSerializer(TCPScanEvent)
    event_serializer_registry[PropagationEvent] = PydanticAgentEventSerializer(PropagationEvent)
    event_serializer_registry[ExploitationEvent] = PydanticAgentEventSerializer(ExploitationEvent)
    event_serializer_registry[PasswordRestorationEvent] = PydanticAgentEventSerializer(
        PasswordRestorationEvent
    )
    event_serializer_registry[AgentShutdownEvent] = PydanticAgentEventSerializer(AgentShutdownEvent)
    event_serializer_registry[FileEncryptionEvent] = PydanticAgentEventSerializer(
        FileEncryptionEvent
    )
    event_serializer_registry[OSDiscoveryEvent] = PydanticAgentEventSerializer(OSDiscoveryEvent)
    event_serializer_registry[HostnameDiscoveryEvent] = PydanticAgentEventSerializer(
        HostnameDiscoveryEvent
    )

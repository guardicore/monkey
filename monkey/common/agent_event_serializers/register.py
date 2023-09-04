from common.agent_events import (
    AgentShutdownEvent,
    CPUConsumptionEvent,
    CredentialsStolenEvent,
    ExploitationEvent,
    FileEncryptionEvent,
    FingerprintingEvent,
    HostnameDiscoveryEvent,
    HTTPRequestEvent,
    OSDiscoveryEvent,
    PasswordRestorationEvent,
    PingScanEvent,
    PropagationEvent,
    RAMConsumptionEvent,
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
    event_serializer_registry[FingerprintingEvent] = PydanticAgentEventSerializer(
        FingerprintingEvent
    )
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
    event_serializer_registry[CPUConsumptionEvent] = PydanticAgentEventSerializer(
        CPUConsumptionEvent
    )
    event_serializer_registry[RAMConsumptionEvent] = PydanticAgentEventSerializer(
        RAMConsumptionEvent
    )
    event_serializer_registry[HTTPRequestEvent] = PydanticAgentEventSerializer(HTTPRequestEvent)

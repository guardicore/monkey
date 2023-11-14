from common.agent_events import (
    AgentShutdownEvent,
    CPUConsumptionEvent,
    CredentialsStolenEvent,
    DefacementEvent,
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

from . import AgentEventRegistry


def register_common_agent_events(
    agent_event_registry: AgentEventRegistry,
):
    agent_event_registry.register(AgentShutdownEvent)
    agent_event_registry.register(CPUConsumptionEvent)
    agent_event_registry.register(CredentialsStolenEvent)
    agent_event_registry.register(DefacementEvent)
    agent_event_registry.register(ExploitationEvent)
    agent_event_registry.register(FileEncryptionEvent)
    agent_event_registry.register(FingerprintingEvent)
    agent_event_registry.register(HostnameDiscoveryEvent)
    agent_event_registry.register(HTTPRequestEvent)
    agent_event_registry.register(OSDiscoveryEvent)
    agent_event_registry.register(PasswordRestorationEvent)
    agent_event_registry.register(PingScanEvent)
    agent_event_registry.register(PropagationEvent)
    agent_event_registry.register(RAMConsumptionEvent)
    agent_event_registry.register(TCPScanEvent)

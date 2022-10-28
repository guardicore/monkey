from common.agent_events import (
    AgentShutdownEvent,
    CredentialsStolenEvent,
    ExploitationEvent,
    FileEncryptionEvent,
    PasswordRestorationEvent,
    PingScanEvent,
    PropagationEvent,
    TCPScanEvent,
)

from . import AgentEventRegistry


def register_common_agent_events(
    agent_event_registry: AgentEventRegistry,
):
    agent_event_registry.register(CredentialsStolenEvent)
    agent_event_registry.register(PingScanEvent)
    agent_event_registry.register(TCPScanEvent)
    agent_event_registry.register(PropagationEvent)
    agent_event_registry.register(ExploitationEvent)
    agent_event_registry.register(PasswordRestorationEvent)
    agent_event_registry.register(AgentShutdownEvent)
    agent_event_registry.register(FileEncryptionEvent)

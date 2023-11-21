from . import AgentEventRegistry
from .builtin_agent_events import BUILTIN_AGENT_EVENT_CLASSES


def register_common_agent_events(
    agent_event_registry: AgentEventRegistry,
):
    for event_class in BUILTIN_AGENT_EVENT_CLASSES:
        agent_event_registry.register(event_class)

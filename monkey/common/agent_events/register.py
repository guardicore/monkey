import inspect

import monkeyevents

from . import AgentEventRegistry


def register_common_agent_events(
    agent_event_registry: AgentEventRegistry,
):
    for _, event_class in inspect.getmembers(monkeyevents, inspect.isclass):
        if event_class is monkeyevents.AbstractAgentEvent:
            continue

        if not issubclass(event_class, monkeyevents.AbstractAgentEvent):
            continue

        agent_event_registry.register(event_class)

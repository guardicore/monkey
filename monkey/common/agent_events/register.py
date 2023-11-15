import inspect

import common.agent_events

from . import AgentEventRegistry


def register_common_agent_events(
    agent_event_registry: AgentEventRegistry,
):
    for _, event_class in inspect.getmembers(common.agent_events, inspect.isclass):
        if event_class is common.agent_events.AbstractAgentEvent:
            continue

        if not issubclass(event_class, common.agent_events.AbstractAgentEvent):
            continue

        agent_event_registry.register(event_class)

import inspect

import common.agent_events

from . import AgentEventSerializerRegistry, PydanticAgentEventSerializer


def register_common_agent_event_serializers(
    event_serializer_registry: AgentEventSerializerRegistry,
):
    for _, event_class in inspect.getmembers(common.agent_events, inspect.isclass):
        if event_class is common.agent_events.AbstractAgentEvent:
            continue

        if not issubclass(event_class, common.agent_events.AbstractAgentEvent):
            continue

        event_serializer_registry[event_class] = PydanticAgentEventSerializer(event_class)

import inspect

import common.agent_events

from . import AgentEventSerializerRegistry, PydanticAgentEventSerializer


def register_common_agent_event_serializers(
    event_serializer_registry: AgentEventSerializerRegistry,
):
    for name, event_class in inspect.getmembers(common.agent_events, inspect.isclass):
        if name == "AbstractAgentEvent":
            continue

        if not issubclass(event_class, common.agent_events.AbstractAgentEvent):
            continue

        event_serializer_registry[event_class] = PydanticAgentEventSerializer(event_class)

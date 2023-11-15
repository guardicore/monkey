import inspect

import common.agent_events

from . import AgentEventSerializerRegistry, PydanticAgentEventSerializer


def register_common_agent_event_serializers(
    event_serializer_registry: AgentEventSerializerRegistry,
):
    # Note: The code to identify all agent events here duplicates the code from
    # common.agent_events.register_common_agent_events(). This is difficult to rectify at the
    # present time without introducing a circular import. This should be fixable once #3799 is
    # completed and agent events are moved to the monkeyevents package.
    for _, event_class in inspect.getmembers(common.agent_events, inspect.isclass):
        if event_class is common.agent_events.AbstractAgentEvent:
            continue

        if not issubclass(event_class, common.agent_events.AbstractAgentEvent):
            continue

        event_serializer_registry[event_class] = PydanticAgentEventSerializer(event_class)

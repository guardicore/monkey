import inspect

import monkeyevents
from monkeyevents import PydanticAgentEventSerializer

from . import AgentEventSerializerRegistry


def register_common_agent_event_serializers(
    event_serializer_registry: AgentEventSerializerRegistry,
):
    # Note: The code to identify all agent events here duplicates the code from
    # common.agent_events.register_common_agent_events(). This is difficult to rectify at the
    # present time without introducing a circular import. This should be fixable once #3799 is
    # completed and agent events are moved to the monkeyevents package.
    for _, event_class in inspect.getmembers(monkeyevents, inspect.isclass):
        if event_class is monkeyevents.AbstractAgentEvent:
            continue

        if not issubclass(event_class, monkeyevents.AbstractAgentEvent):
            continue

        event_serializer_registry[event_class] = PydanticAgentEventSerializer(event_class)

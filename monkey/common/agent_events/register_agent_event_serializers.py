from monkeyevents import PydanticAgentEventSerializer

from . import AgentEventSerializerRegistry
from .builtin_agent_events import BUILTIN_AGENT_EVENT_CLASSES


def register_builtin_agent_event_serializers(
    event_serializer_registry: AgentEventSerializerRegistry,
):
    for event_class in BUILTIN_AGENT_EVENT_CLASSES:
        event_serializer_registry[event_class] = PydanticAgentEventSerializer(event_class)

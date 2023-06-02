from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    PydanticAgentEventSerializer,
)
from common.di_container import DIContainer
from common.event_queue import IAgentEventQueue

from .message_event import MessageEvent


def handle_message_event(event: MessageEvent):
    print(f"Received event: {event.message}")


class Events:
    def register_event_serializers(self, event_serializer_registry: AgentEventSerializerRegistry):
        event_serializer_registry[MessageEvent] = PydanticAgentEventSerializer(MessageEvent)

    def register_event_handlers(
        self, di_container: DIContainer, agent_event_queue: IAgentEventQueue
    ):
        agent_event_queue.subscribe_type(MessageEvent, handle_message_event)

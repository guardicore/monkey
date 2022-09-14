import logging
from http import HTTPStatus

from flask import request

from common.event_queue import IAgentEventQueue
from common.event_serializers import EVENT_TYPE_FIELD, EventSerializerRegistry
from monkey_island.cc.resources.AbstractResource import AbstractResource

logger = logging.getLogger(__name__)


class Events(AbstractResource):
    urls = ["/api/events"]

    def __init__(
        self,
        agent_event_queue: IAgentEventQueue,
        event_serializer_registry: EventSerializerRegistry,
    ):
        self._agent_event_queue = agent_event_queue
        self._event_serializer_registry = event_serializer_registry

    # Agents needs this
    def post(self):
        events = request.json

        for event in events:
            try:
                serializer = self._event_serializer_registry[event[EVENT_TYPE_FIELD]]
                deserialized_event = serializer.deserialize(event)
            except (TypeError, ValueError) as err:
                logger.debug(f"Error occured deserializing an event {event}: {err}")
                return {"error": str(err)}, HTTPStatus.BAD_REQUEST

            self._agent_event_queue.publish(deserialized_event)

        return {}, HTTPStatus.NO_CONTENT

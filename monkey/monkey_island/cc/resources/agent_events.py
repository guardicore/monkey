import logging
from http import HTTPStatus
from typing import Iterable

from flask import request

from common.agent_event_serializers import EVENT_TYPE_FIELD, AgentEventSerializerRegistry
from common.agent_events import AbstractAgentEvent
from common.event_queue import IAgentEventQueue
from common.types import JSONSerializable
from monkey_island.cc.repository import IAgentEventRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource

logger = logging.getLogger(__name__)


class AgentEvents(AbstractResource):
    urls = ["/api/agent-events"]

    def __init__(
        self,
        agent_event_queue: IAgentEventQueue,
        event_serializer_registry: AgentEventSerializerRegistry,
        agent_event_repository: IAgentEventRepository,
    ):
        self._agent_event_queue = agent_event_queue
        self._event_serializer_registry = event_serializer_registry
        self._agent_event_repository = agent_event_repository

    # Agents needs this
    def post(self):
        events = request.json

        for event in events:
            try:
                serializer = self._event_serializer_registry[event[EVENT_TYPE_FIELD]]
                deserialized_event = serializer.deserialize(event)
            except (TypeError, ValueError) as err:
                logger.exception(f"Error occurred while deserializing an event {event}: {err}")
                return {"error": str(err)}, HTTPStatus.BAD_REQUEST

            self._agent_event_queue.publish(deserialized_event)

        return {}, HTTPStatus.NO_CONTENT

    def get(self):
        events = self._agent_event_repository.get_events()

        try:
            serialized_events = self._serialize_events(events)
        except (TypeError, ValueError) as err:
            return {"error": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR

        return serialized_events, HTTPStatus.OK

    def _serialize_events(self, events: Iterable[AbstractAgentEvent]) -> JSONSerializable:
        serialized_events = []

        for event in events:
            try:
                serializer = self._event_serializer_registry[event.__class__]
                serialized_event = serializer.serialize(event)
                serialized_events.append(serialized_event)
            except (TypeError, ValueError) as err:
                logger.exception(f"Error occurred while serializing an event {event}: {err}")
                raise err

        return serialized_events

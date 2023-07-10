import logging
from bisect import bisect_left, bisect_right
from http import HTTPStatus
from typing import Iterable, Optional, Sequence, Tuple, Type

from flask import request
from flask_security import auth_token_required, roles_accepted

from common.agent_event_serializers import EVENT_TYPE_FIELD, AgentEventSerializerRegistry
from common.agent_events import AbstractAgentEvent, AgentEventRegistry
from common.event_queue import IAgentEventQueue
from common.types import JSONSerializable
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.repositories import IAgentEventRepository
from monkey_island.cc.services.authentication_service import AccountRole

logger = logging.getLogger(__name__)


class AgentEvents(AbstractResource):
    urls = ["/api/agent-events"]

    def __init__(
        self,
        agent_event_queue: IAgentEventQueue,
        event_serializer_registry: AgentEventSerializerRegistry,
        agent_event_repository: IAgentEventRepository,
        agent_event_registry: AgentEventRegistry,
    ):
        self._agent_event_queue = agent_event_queue
        self._event_serializer_registry = event_serializer_registry
        self._agent_event_repository = agent_event_repository
        self._agent_event_registry = agent_event_registry

    @auth_token_required
    @roles_accepted(AccountRole.AGENT.name)
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

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def get(self):
        try:
            type_, success, timestamp_constraint = self._parse_event_filter_args()
        except Exception as err:
            return {"error": str(err)}, HTTPStatus.UNPROCESSABLE_ENTITY

        events = self._get_filtered_events(type_, success, timestamp_constraint)

        try:
            serialized_events = self._serialize_events(events)
        except (TypeError, ValueError) as err:
            return {"error": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR

        return serialized_events, HTTPStatus.OK

    def _parse_event_filter_args(
        self,
    ) -> Tuple[Optional[Type[AbstractAgentEvent]], Optional[bool], Optional[Tuple[str, str]]]:
        type_arg = request.args.get("type", None)
        success_arg = request.args.get("success", None)
        timestamp_arg = request.args.get("timestamp", None)

        try:
            type_ = None if type_arg is None else self._agent_event_registry[type_arg]
        except KeyError:
            raise Exception(f'Unknown agent event type "{type_}"')

        if success_arg is None:
            success = None
        elif success_arg == "true":
            success = True
        elif success_arg == "false":
            success = False
        else:
            raise Exception(
                f'Invalid value for success "{success_arg}", expected "true" or "false"'
            )

        if timestamp_arg:
            operator, timestamp = timestamp_arg.split(":")
            if not operator or not timestamp or operator not in ("gt", "lt"):
                raise Exception(f'Invalid timestamp argument "{timestamp_arg}"')
            timestamp_constraint = (operator, timestamp)
        else:
            timestamp_constraint = None

        return type_, success, timestamp_constraint

    def _get_filtered_events(
        self,
        type_: Optional[Type[AbstractAgentEvent]],
        success: Optional[bool],
        timestamp_constraint: Optional[Tuple[str, str]],
    ) -> Sequence[AbstractAgentEvent]:
        if type_ is not None:
            events: Sequence[AbstractAgentEvent] = self._agent_event_repository.get_events_by_type(
                type_
            )
        else:
            events = self._agent_event_repository.get_events()

        if success is not None:
            events = list(filter(lambda e: hasattr(e, "success") and e.success is success, events))  # type: ignore[attr-defined]  # noqa: E501

        if timestamp_constraint is not None:
            operator, timestamp = timestamp_constraint
            if operator == "gt":
                separation_point = bisect_right(
                    events, float(timestamp), key=lambda event: event.timestamp
                )
                events = events[separation_point:]
            elif operator == "lt":
                separation_point = bisect_left(
                    events, float(timestamp), key=lambda event: event.timestamp
                )
                events = events[:separation_point]

        return events

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

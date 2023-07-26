import logging
import re
from bisect import bisect_left, bisect_right
from http import HTTPStatus
from typing import Iterable, Optional, Sequence, Tuple, Type

from flask import request
from flask_security import auth_token_required, roles_accepted

from common.agent_event_serializers import EVENT_TYPE_FIELD, AgentEventSerializerRegistry
from common.agent_events import EVENT_TAG_REGEX, AbstractAgentEvent, AgentEventRegistry
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
        serialized_events = request.json
        deserialized_events = []

        logger.debug(f"Deserializing {len(serialized_events)} events")
        for event in serialized_events:
            try:
                serializer = self._event_serializer_registry[event[EVENT_TYPE_FIELD]]
                deserialized_events.append(serializer.deserialize(event))
            except (TypeError, ValueError) as err:
                logger.exception(f"Error occurred while deserializing an event {event}: {err}")
                return {"error": str(err)}, HTTPStatus.BAD_REQUEST
        logger.debug(f"Completed deserialization of {len(serialized_events)} events")

        logger.debug(f"Publishing {len(deserialized_events)} events to the queue")
        for deserialized_event in deserialized_events:
            self._agent_event_queue.publish(deserialized_event)
        logger.debug(f"Completed publishing {len(deserialized_events)} events to the queue")

        return {}, HTTPStatus.NO_CONTENT

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def get(self):
        try:
            type_, tag, success, timestamp_constraint = self._parse_event_filter_args()
        except Exception as err:
            return {"error": str(err)}, HTTPStatus.UNPROCESSABLE_ENTITY

        events = self._get_filtered_events(type_, tag, success, timestamp_constraint)

        try:
            serialized_events = self._serialize_events(events)
        except (TypeError, ValueError) as err:
            return {"error": str(err)}, HTTPStatus.INTERNAL_SERVER_ERROR

        return serialized_events, HTTPStatus.OK

    def _parse_event_filter_args(
        self,
    ) -> Tuple[
        Optional[Type[AbstractAgentEvent]],
        Optional[str],
        Optional[bool],
        Optional[Tuple[str, float]],
    ]:
        type_arg = request.args.get("type", None)
        tag_arg = request.args.get("tag", None)
        success_arg = request.args.get("success", None)
        timestamp_arg = request.args.get("timestamp", None)

        type_ = self._parse_type_arg(type_arg)
        tag = self._parse_tag_arg(tag_arg)
        success = self._parse_success_arg(success_arg)
        timestamp_constraint = self._parse_timestamp_arg(timestamp_arg)

        return type_, tag, success, timestamp_constraint

    def _parse_type_arg(self, type_arg: Optional[str]) -> Optional[Type[AbstractAgentEvent]]:
        try:
            type_ = None if type_arg is None else self._agent_event_registry[type_arg]
        except KeyError:
            raise ValueError(f'Unknown agent event type "{type_arg}"')

        return type_

    def _parse_tag_arg(self, tag_arg: Optional[str]) -> Optional[str]:
        if tag_arg and not re.match(pattern=re.compile(EVENT_TAG_REGEX), string=tag_arg):
            raise ValueError(f'Invalid event tag "{tag_arg}"')

        return tag_arg

    def _parse_success_arg(self, success_arg: Optional[str]) -> Optional[bool]:
        if success_arg is None:
            success = None
        elif success_arg == "true":
            success = True
        elif success_arg == "false":
            success = False
        else:
            raise ValueError(
                f'Invalid value for success "{success_arg}", expected "true" or "false"'
            )

        return success

    def _parse_timestamp_arg(self, timestamp_arg: Optional[str]) -> Optional[Tuple[str, float]]:
        if timestamp_arg is None:
            timestamp_constraint = None
        else:
            operator, timestamp = timestamp_arg.split(":")
            if not operator or not timestamp or operator not in ("gt", "lt"):
                raise ValueError(
                    f'Invalid timestamp argument "{timestamp_arg}", '
                    'expected format: "{gt,lt}:<timestamp>"'
                )
            try:
                timestamp_constraint = (operator, float(timestamp))
            except Exception:
                raise ValueError(
                    f'Invalid timestamp argument "{timestamp_arg}", '
                    "expected timestamp to be a number"
                )

        return timestamp_constraint

    def _get_filtered_events(
        self,
        type_: Optional[Type[AbstractAgentEvent]],
        tag: Optional[str],
        success: Optional[bool],
        timestamp_constraint: Optional[Tuple[str, float]],
    ) -> Sequence[AbstractAgentEvent]:
        if type_ is not None and tag is not None:
            events = self._get_events_filtered_by_type_and_tag(type_, tag)
        elif type_ is not None and tag is None:
            events = self._agent_event_repository.get_events_by_type(type_)
        elif type_ is None and tag is not None:
            events = self._agent_event_repository.get_events_by_tag(tag)
        else:
            events = self._agent_event_repository.get_events()

        if success is not None:
            events = self._filter_events_by_success(events, success)

        if timestamp_constraint is not None:
            events = self._filter_events_by_timestamp(events, timestamp_constraint)

        return events

    def _get_events_filtered_by_type_and_tag(
        self, type_: Type[AbstractAgentEvent], tag: str
    ) -> Sequence[AbstractAgentEvent]:
        events_by_type = set(self._agent_event_repository.get_events_by_type(type_))
        events_by_tag = set(self._agent_event_repository.get_events_by_tag(tag))

        intersection = events_by_type.intersection(events_by_tag)
        return sorted(intersection, key=lambda x: x.timestamp)

    def _filter_events_by_success(
        self, events: Sequence[AbstractAgentEvent], success: bool
    ) -> Sequence[AbstractAgentEvent]:
        return list(filter(lambda e: hasattr(e, "success") and e.success is success, events))

    def _filter_events_by_timestamp(
        self, events: Sequence[AbstractAgentEvent], timestamp_constraint: Tuple[str, float]
    ) -> Sequence[AbstractAgentEvent]:
        operator, timestamp = timestamp_constraint

        bisect_fn = bisect_left if operator == "lt" else bisect_right
        separation_point = bisect_fn(events, timestamp, key=lambda event: event.timestamp)

        if operator == "lt":
            return events[:separation_point]

        return events[separation_point:]

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

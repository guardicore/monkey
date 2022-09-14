from http import HTTPStatus
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.common import StubDIContainer

from common.event_queue import IAgentEventQueue
from common.event_serializers import EventSerializerRegistry, PydanticEventSerializer
from common.events import AbstractAgentEvent
from monkey_island.cc.resources import Events

EVENTS_URL = Events.urls[0]


class SomeAgentEvent(AbstractAgentEvent):
    some_field: int


class OtherAgentEvent(AbstractAgentEvent):
    other_field: float


class DifferentAgentEvent(AbstractAgentEvent):
    different_field: str


SERIALIZED_EVENT_1 = {
    "type": SomeAgentEvent.__name__,
    "some_field": 1,
    "source": UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5"),
    "target": None,
    "timestamp": 0.0,
    "tags": ["some-event"],
}

EXPECTED_EVENT_1 = SomeAgentEvent(
    some_field=1,
    source=UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5"),
    target=None,
    timestamp=0.0,
    tags=frozenset({"some-event"}),
)

SERIALIZED_EVENT_2 = {
    "type": OtherAgentEvent.__name__,
    "other_field": 2.0,
    "source": UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10"),
    "target": None,
    "timestamp": 1.0,
    "tags": [],
}

EXPECTED_EVENT_2 = OtherAgentEvent(
    other_field=2.0,
    source=UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10"),
    target=None,
    timestamp=1.0,
    tags=frozenset(),
)

SERIALIZED_EVENT_3 = {
    "type": DifferentAgentEvent.__name__,
    "different_field": "some_data",
    "source": UUID("0fc9afcb-1902-436b-bd5c-1ad194252484"),
    "target": None,
    "timestamp": 2.0,
    "tags": ["some-event3"],
}

EXPECTED_EVENT_3 = DifferentAgentEvent(
    different_field="some_data",
    source=UUID("0fc9afcb-1902-436b-bd5c-1ad194252484"),
    target=None,
    timestamp=2.0,
    tags=frozenset({"some-event3"}),
)


LIST_EVENTS = [SERIALIZED_EVENT_1, SERIALIZED_EVENT_2, SERIALIZED_EVENT_3]

EXPECTED_EVENTS = [EXPECTED_EVENT_1, EXPECTED_EVENT_2, EXPECTED_EVENT_3]


@pytest.fixture
def mock_agent_event_queue():
    return MagicMock(spec=IAgentEventQueue)


@pytest.fixture
def event_serializer_registry() -> EventSerializerRegistry:
    event_serializer_registry = EventSerializerRegistry()
    event_serializer_registry[SomeAgentEvent] = PydanticEventSerializer(SomeAgentEvent)
    event_serializer_registry[OtherAgentEvent] = PydanticEventSerializer(OtherAgentEvent)
    event_serializer_registry[DifferentAgentEvent] = PydanticEventSerializer(DifferentAgentEvent)

    return event_serializer_registry


@pytest.fixture
def flask_client(build_flask_client, mock_agent_event_queue, event_serializer_registry):
    container = StubDIContainer()

    container.register_instance(IAgentEventQueue, mock_agent_event_queue)
    container.register_instance(EventSerializerRegistry, event_serializer_registry)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_events_endpoint(flask_client, mock_agent_event_queue):

    response = flask_client.post(EVENTS_URL, json=LIST_EVENTS)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert mock_agent_event_queue.publish.call_count == len(EXPECTED_EVENTS)

    for call_args in mock_agent_event_queue.publish.call_args_list:
        assert call_args[0][0] in EXPECTED_EVENTS


@pytest.mark.parametrize(
    "events, expected_status_code",
    [(["bogus", "vogus"], HTTPStatus.BAD_REQUEST), ([], HTTPStatus.NO_CONTENT)],
)
def test_events_endpoint__bogus_events(
    flask_client, mock_agent_event_queue, events, expected_status_code
):
    response = flask_client.post(EVENTS_URL, json=events)

    assert response.status_code == expected_status_code
    mock_agent_event_queue.publish.not_called()

from http import HTTPStatus
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.common import StubDIContainer

from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    PydanticAgentEventSerializer,
)
from common.agent_events import AbstractAgentEvent
from common.event_queue import IAgentEventQueue
from monkey_island.cc.repository import IAgentEventRepository
from monkey_island.cc.resources import AgentEvents

AGENT_EVENTS_URL = AgentEvents.urls[0]


class SomeAgentEvent(AbstractAgentEvent):
    some_field: int


class OtherAgentEvent(AbstractAgentEvent):
    other_field: float


class DifferentAgentEvent(AbstractAgentEvent):
    different_field: str


SERIALIZED_EVENT_1 = {
    "type": SomeAgentEvent.__name__,
    "some_field": 1,
    "source": "f811ad00-5a68-4437-bd51-7b5cc1768ad5",
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
    "source": "012e7238-7b81-4108-8c7f-0787bc3f3c10",
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
    "source": "0fc9afcb-1902-436b-bd5c-1ad194252484",
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
def error_raising_event_serializer_registry():
    error_raising_event_serializer_registry = MagicMock(spec=AgentEventSerializerRegistry)
    error_raising_event_serializer_registry.__getitem__ = MagicMock(side_effect=KeyError)

    return error_raising_event_serializer_registry


@pytest.fixture
def agent_event_repository():
    agent_event_repository = MagicMock(spec=IAgentEventRepository)
    agent_event_repository.get_events = MagicMock(return_value=EXPECTED_EVENTS)

    return agent_event_repository


@pytest.fixture
def event_serializer_registry() -> AgentEventSerializerRegistry:
    event_serializer_registry = AgentEventSerializerRegistry()
    event_serializer_registry[SomeAgentEvent] = PydanticAgentEventSerializer(SomeAgentEvent)
    event_serializer_registry[OtherAgentEvent] = PydanticAgentEventSerializer(OtherAgentEvent)
    event_serializer_registry[DifferentAgentEvent] = PydanticAgentEventSerializer(
        DifferentAgentEvent
    )

    return event_serializer_registry


@pytest.fixture
def flask_client(
    build_flask_client, mock_agent_event_queue, event_serializer_registry, agent_event_repository
):
    container = StubDIContainer()

    container.register_instance(IAgentEventQueue, mock_agent_event_queue)
    container.register_instance(AgentEventSerializerRegistry, event_serializer_registry)
    container.register_instance(IAgentEventRepository, agent_event_repository)

    with build_flask_client(container) as flask_client:
        yield flask_client


@pytest.fixture
def error_raising_flask_client(
    build_flask_client,
    mock_agent_event_queue,
    agent_event_repository,
    error_raising_event_serializer_registry,
):
    container = StubDIContainer()

    container.register_instance(IAgentEventQueue, mock_agent_event_queue)
    container.register_instance(
        AgentEventSerializerRegistry, error_raising_event_serializer_registry
    )
    container.register_instance(IAgentEventRepository, agent_event_repository)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_agent_events_endpoint__post(flask_client, mock_agent_event_queue):
    resp_post = flask_client.post(AGENT_EVENTS_URL, json=LIST_EVENTS)

    assert resp_post.status_code == HTTPStatus.NO_CONTENT
    assert mock_agent_event_queue.publish.call_count == len(EXPECTED_EVENTS)

    for call_args in mock_agent_event_queue.publish.call_args_list:
        assert call_args[0][0] in EXPECTED_EVENTS


def test_agent_events_endpoint__get(flask_client):
    resp_get = flask_client.get(AGENT_EVENTS_URL)
    actual_serialized_events = resp_get.json

    assert resp_get.status_code == HTTPStatus.OK
    assert actual_serialized_events == LIST_EVENTS


def test_agent_events_endpoint__get_error(error_raising_flask_client):
    resp_get = error_raising_flask_client.get(AGENT_EVENTS_URL)

    assert resp_get.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.parametrize(
    "events, expected_status_code",
    [(["bogus", "vogus"], HTTPStatus.BAD_REQUEST), ([], HTTPStatus.NO_CONTENT)],
)
def test_agent_events_endpoint__post_bogus_events(
    flask_client, mock_agent_event_queue, events, expected_status_code
):
    resp_post = flask_client.post(AGENT_EVENTS_URL, json=events)

    assert resp_post.status_code == expected_status_code
    mock_agent_event_queue.publish.not_called()

from http import HTTPStatus
from ipaddress import IPv4Address
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.common import StubDIContainer

from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    PydanticAgentEventSerializer,
)
from common.agent_events import AbstractAgentEvent, AgentEventRegistry
from common.event_queue import IAgentEventQueue
from monkey_island.cc.repositories import IAgentEventRepository
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
    "target": 1,
    "timestamp": 0.0,
    "tags": ["some-event"],
}

EXPECTED_EVENT_1 = SomeAgentEvent(
    some_field=1,
    source=UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5"),
    target=1,
    timestamp=0.0,
    tags=frozenset({"some-event"}),
)

SERIALIZED_EVENT_2 = {
    "type": OtherAgentEvent.__name__,
    "other_field": 2.0,
    "source": "012e7238-7b81-4108-8c7f-0787bc3f3c10",
    "target": "127.0.0.1",
    "timestamp": 1.0,
    "tags": [],
}

EXPECTED_EVENT_2 = OtherAgentEvent(
    other_field=2.0,
    source=UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10"),
    target=IPv4Address("127.0.0.1"),
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


class PassFailAgentEvent_type1(AbstractAgentEvent):
    success: bool


class PassFailAgentEvent_type2(AbstractAgentEvent):
    success: bool


PFAE1_1 = PassFailAgentEvent_type1(
    source=UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5"), timestamp=42, success=False, target=1
)
SERIALIZED_PFAE1_1 = {
    "type": PassFailAgentEvent_type1.__name__,
    "success": False,
    "source": "f811ad00-5a68-4437-bd51-7b5cc1768ad5",
    "target": 1,
    "timestamp": 42.0,
    "tags": [],
}
PFAE1_2 = PassFailAgentEvent_type1(
    source=UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5"), timestamp=42, success=True
)
SERIALIZED_PFAE1_2 = {
    "type": PassFailAgentEvent_type1.__name__,
    "success": True,
    "source": "f811ad00-5a68-4437-bd51-7b5cc1768ad5",
    "target": None,
    "timestamp": 42.0,
    "tags": [],
}
PFAE2_1 = PassFailAgentEvent_type2(
    source=UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5"),
    timestamp=42,
    success=True,
    target=IPv4Address("127.0.0.1"),
)
SERIALIZED_PFAE2_1 = {
    "type": PassFailAgentEvent_type2.__name__,
    "success": True,
    "source": "f811ad00-5a68-4437-bd51-7b5cc1768ad5",
    "target": "127.0.0.1",
    "timestamp": 42.0,
    "tags": [],
}


@pytest.fixture
def agent_event_registry() -> AgentEventRegistry:
    agent_event_registry = AgentEventRegistry()

    agent_event_registry.register(SomeAgentEvent)
    agent_event_registry.register(OtherAgentEvent)
    agent_event_registry.register(DifferentAgentEvent)
    agent_event_registry.register(PassFailAgentEvent_type1)
    agent_event_registry.register(PassFailAgentEvent_type2)

    return agent_event_registry


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
    event_serializer_registry[PassFailAgentEvent_type1] = PydanticAgentEventSerializer(
        PassFailAgentEvent_type1
    )
    event_serializer_registry[PassFailAgentEvent_type2] = PydanticAgentEventSerializer(
        PassFailAgentEvent_type2
    )

    return event_serializer_registry


@pytest.fixture
def flask_client(
    build_flask_client,
    mock_agent_event_queue,
    event_serializer_registry,
    agent_event_repository,
    agent_event_registry,
):
    container = StubDIContainer()

    container.register_instance(IAgentEventQueue, mock_agent_event_queue)
    container.register_instance(AgentEventSerializerRegistry, event_serializer_registry)
    container.register_instance(IAgentEventRepository, agent_event_repository)
    container.register_instance(AgentEventRegistry, agent_event_registry)

    with build_flask_client(container) as flask_client:
        yield flask_client


@pytest.fixture
def error_raising_flask_client(
    build_flask_client,
    mock_agent_event_queue,
    agent_event_repository,
    error_raising_event_serializer_registry,
    agent_event_registry,
):
    container = StubDIContainer()

    container.register_instance(IAgentEventQueue, mock_agent_event_queue)
    container.register_instance(
        AgentEventSerializerRegistry, error_raising_event_serializer_registry
    )
    container.register_instance(IAgentEventRepository, agent_event_repository)
    container.register_instance(AgentEventRegistry, agent_event_registry)

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


def test_get_filter__event_type(flask_client, agent_event_repository):
    expected_events = [PFAE1_1, PFAE1_2]
    agent_event_repository.get_events_by_type = MagicMock(return_value=expected_events)

    resp_get = flask_client.get(AGENT_EVENTS_URL + "?type=PassFailAgentEvent_type1")
    assert resp_get.status_code == HTTPStatus.OK

    assert resp_get.json == [SERIALIZED_PFAE1_1, SERIALIZED_PFAE1_2]


def test_get_filter__success_true(flask_client, agent_event_repository):
    agent_event_repository.get_events = MagicMock(return_value=[PFAE1_1, PFAE1_2, PFAE2_1])

    resp_get = flask_client.get(AGENT_EVENTS_URL + "?success=true")
    assert resp_get.status_code == HTTPStatus.OK

    assert resp_get.json == [SERIALIZED_PFAE1_2, SERIALIZED_PFAE2_1]


def test_get_filter__success_false(flask_client, agent_event_repository):
    agent_event_repository.get_events = MagicMock(return_value=[PFAE1_1, PFAE1_2, PFAE2_1])

    resp_get = flask_client.get(AGENT_EVENTS_URL + "?success=false")
    assert resp_get.status_code == HTTPStatus.OK

    assert resp_get.json == [SERIALIZED_PFAE1_1]


def test_get_filter__event_missing_success(flask_client, agent_event_repository):
    agent_event_repository.get_events = MagicMock(
        return_value=[PFAE1_1, PFAE1_2, PFAE2_1, EXPECTED_EVENT_1, EXPECTED_EVENT_2]
    )

    resp_get = flask_client.get(AGENT_EVENTS_URL + "?success=false")
    assert resp_get.status_code == HTTPStatus.OK

    assert resp_get.json == [SERIALIZED_PFAE1_1]


def test_get_filter__type_and_success(flask_client, agent_event_repository):
    agent_event_repository.get_events_by_type = MagicMock(return_value=[PFAE1_1, PFAE1_2])

    resp_get = flask_client.get(AGENT_EVENTS_URL + "?type=PassFailAgentEvent_type1&success=true")
    assert resp_get.status_code == HTTPStatus.OK

    assert resp_get.json == [SERIALIZED_PFAE1_2]


def test_get_filter__unknown_type(flask_client, agent_event_repository):
    resp_get = flask_client.get(AGENT_EVENTS_URL + "?type=UnknownEventType")
    assert resp_get.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_filter__invalid_success(flask_client, agent_event_repository):
    resp_get = flask_client.get(AGENT_EVENTS_URL + "?success=bogus")
    assert resp_get.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


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

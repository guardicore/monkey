import uuid
from typing import List
from unittest.mock import MagicMock

import mongomock
import pytest

from monkey.common.events.abstract_agent_event import AbstractAgentEvent
from monkey.monkey_island.cc.repository import (
    IEventRepository,
    MongoEventRepository,
    RemovalError,
    RetrievalError,
    StorageError,
)


class FakeAgentEvent(AbstractAgentEvent):
    item: str


EVENTS: List[AbstractAgentEvent] = [
    AbstractAgentEvent(source=uuid.uuid4(), tags={"foo"}),
    AbstractAgentEvent(source=uuid.uuid4(), tags={"foo", "bar"}),
    AbstractAgentEvent(source=uuid.uuid4(), tags={"bar", "baz"}),
    FakeAgentEvent(source=uuid.uuid4(), tags={"baz"}, item="blah"),
]


@pytest.fixture
def mongo_client():
    client = mongomock.MongoClient()
    client.monkey_island.events.insert_many((e.dict(simplify=True) for e in EVENTS))
    return client


@pytest.fixture
def mongo_repository(mongo_client) -> IEventRepository:
    return MongoEventRepository(mongo_client)


@pytest.fixture
def error_raising_mongo_client(mongo_client) -> mongomock.MongoClient:
    mongo_client = MagicMock(spec=mongomock.MongoClient)
    mongo_client.monkey_island = MagicMock(spec=mongomock.Database)
    mongo_client.monkey_island.events = MagicMock(spec=mongomock.Collection)

    # The first call to find() must succeed
    mongo_client.monkey_island.events.find = MagicMock(
        # side_effect=chain([MagicMock()], repeat(Exception("some exception")))
        side_effect=Exception("some exception")
    )
    mongo_client.monkey_island.events.find_one = MagicMock(side_effect=Exception("some exception"))
    mongo_client.monkey_island.events.insert_one = MagicMock(
        side_effect=Exception("some exception")
    )
    mongo_client.monkey_island.events.replace_one = MagicMock(
        side_effect=Exception("some exception")
    )
    mongo_client.monkey_island.events.drop = MagicMock(side_effect=Exception("some exception"))

    return mongo_client


@pytest.fixture
def error_raising_mongo_repository(error_raising_mongo_client) -> IEventRepository:
    return MongoEventRepository(error_raising_mongo_client)


def assert_same_contents(a, b):
    assert len(a) == len(b)
    difference = set(a) ^ set(b)
    assert not difference


def test_mongo_event_repository__save_event(mongo_repository: IEventRepository):
    event = AbstractAgentEvent(source=uuid.uuid4())
    mongo_repository.save_event(event)
    events = mongo_repository.get_events()

    assert event in events


def test_mongo_event_repository__save_event_raises(
    error_raising_mongo_repository: IEventRepository,
):
    event = AbstractAgentEvent(source=uuid.uuid4())

    with pytest.raises(StorageError):
        error_raising_mongo_repository.save_event(event)


def test_mongo_event_repository__get_events(mongo_repository: IEventRepository):
    events = mongo_repository.get_events()

    assert_same_contents(events, EVENTS)


def test_mongo_event_repository__get_events_raises(
    error_raising_mongo_repository: IEventRepository,
):
    with pytest.raises(RetrievalError):
        error_raising_mongo_repository.get_events()


def test_mongo_event_repository__get_events_by_type(mongo_repository: IEventRepository):
    events = mongo_repository.get_events_by_type(FakeAgentEvent)

    expected_events = [EVENTS[3]]
    assert_same_contents(events, expected_events)


def test_mongo_event_repository__get_events_by_type_raises(
    error_raising_mongo_repository: IEventRepository,
):
    with pytest.raises(RetrievalError):
        error_raising_mongo_repository.get_events_by_type(FakeAgentEvent)


def test_mongo_event_repository__get_events_by_tag(mongo_repository: IEventRepository):
    events = mongo_repository.get_events_by_tag("bar")

    expected_events = [EVENTS[1], EVENTS[2]]
    assert_same_contents(events, expected_events)


def test_mongo_event_repository__get_events_by_tag_raises(
    error_raising_mongo_repository: IEventRepository,
):
    with pytest.raises(RetrievalError):
        error_raising_mongo_repository.get_events_by_tag("bar")


def test_mongo_event_repository__get_events_by_source(mongo_repository: IEventRepository):
    source_event = EVENTS[2]
    events = mongo_repository.get_events_by_source(source_event.source)

    expected_events = [source_event]
    assert_same_contents(events, expected_events)


def test_mongo_event_repository__get_events_by_source_raises(
    error_raising_mongo_repository: IEventRepository,
):
    with pytest.raises(RetrievalError):
        source_event = EVENTS[2]
        error_raising_mongo_repository.get_events_by_source(source_event.source)


def test_mongo_event_repository__reset(mongo_repository: IEventRepository):
    mongo_repository.reset()
    events = mongo_repository.get_events()

    assert not events


def test_mongo_event_repository__reset_raises(error_raising_mongo_repository: IEventRepository):
    with pytest.raises(RemovalError):
        error_raising_mongo_repository.reset()

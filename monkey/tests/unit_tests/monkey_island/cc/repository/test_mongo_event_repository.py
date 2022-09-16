import uuid
from typing import List
from unittest.mock import MagicMock

import mongomock
import pytest
from pydantic import Field

from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    PydanticAgentEventSerializer,
)
from common.agent_events import AbstractAgentEvent
from monkey_island.cc.repository import (
    IAgentEventRepository,
    MongoEventRepository,
    RemovalError,
    RetrievalError,
    StorageError,
)
from monkey_island.cc.server_utils.encryption import RepositoryEncryptor


class FakeAgentEvent(AbstractAgentEvent):
    data = Field(default=435)


class FakeAgentItemEvent(AbstractAgentEvent):
    item: str


EVENTS: List[AbstractAgentEvent] = [
    FakeAgentEvent(source=uuid.uuid4(), tags={"foo"}),
    FakeAgentEvent(source=uuid.uuid4(), tags={"foo", "bar"}),
    FakeAgentEvent(source=uuid.uuid4(), tags={"bar", "baz"}),
    FakeAgentItemEvent(source=uuid.uuid4(), tags={"baz"}, item="blah"),
]


@pytest.fixture
def event_serializer_registry() -> AgentEventSerializerRegistry:
    registry = AgentEventSerializerRegistry()
    registry[FakeAgentEvent] = PydanticAgentEventSerializer(FakeAgentEvent)
    registry[FakeAgentItemEvent] = PydanticAgentEventSerializer(FakeAgentItemEvent)
    return registry


@pytest.fixture
def mongo_client(event_serializer_registry):
    client = mongomock.MongoClient()
    client.monkey_island.events.insert_many(
        (event_serializer_registry[type(e)].serialize(e) for e in EVENTS)
    )
    return client


@pytest.fixture
def key_file(tmp_path):
    return tmp_path / "test_key.bin"


@pytest.fixture
def encryptor(key_file):
    encryptor = RepositoryEncryptor(key_file)
    encryptor.unlock(b"password")
    return encryptor


@pytest.fixture
def mongo_repository(mongo_client, event_serializer_registry, encryptor) -> IAgentEventRepository:
    return MongoEventRepository(mongo_client, event_serializer_registry, encryptor)


@pytest.fixture
def error_raising_mongo_client(mongo_client) -> mongomock.MongoClient:
    mongo_client = MagicMock(spec=mongomock.MongoClient)
    mongo_client.monkey_island = MagicMock(spec=mongomock.Database)
    mongo_client.monkey_island.events = MagicMock(spec=mongomock.Collection)

    mongo_client.monkey_island.events.find = MagicMock(side_effect=Exception("some exception"))
    mongo_client.monkey_island.events.insert_one = MagicMock(
        side_effect=Exception("some exception")
    )
    mongo_client.monkey_island.events.drop = MagicMock(side_effect=Exception("some exception"))

    return mongo_client


@pytest.fixture
def error_raising_mongo_repository(
    error_raising_mongo_client, event_serializer_registry, encryptor
) -> IAgentEventRepository:
    return MongoEventRepository(error_raising_mongo_client, event_serializer_registry, encryptor)


def assert_same_contents(a, b):
    assert len(a) == len(b)
    for item in a:
        assert item in b


def test_mongo_event_repository__save_event(mongo_repository: IAgentEventRepository):
    event = FakeAgentEvent(source=uuid.uuid4())
    mongo_repository.save_event(event)
    events = mongo_repository.get_events()

    assert event in events


def test_mongo_event_repository__save_event_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    event = FakeAgentEvent(source=uuid.uuid4())

    with pytest.raises(StorageError):
        error_raising_mongo_repository.save_event(event)


def test_mongo_event_repository__get_events(mongo_repository: IAgentEventRepository):
    events = mongo_repository.get_events()

    assert_same_contents(events, EVENTS)


def test_mongo_event_repository__get_events_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    with pytest.raises(RetrievalError):
        error_raising_mongo_repository.get_events()


def test_mongo_event_repository__get_events_by_type(mongo_repository: IAgentEventRepository):
    events = mongo_repository.get_events_by_type(FakeAgentItemEvent)

    expected_events = [EVENTS[3]]
    assert_same_contents(events, expected_events)


def test_mongo_event_repository__get_events_by_type_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    with pytest.raises(RetrievalError):
        error_raising_mongo_repository.get_events_by_type(FakeAgentItemEvent)


def test_mongo_event_repository__get_events_by_tag(mongo_repository: IAgentEventRepository):
    events = mongo_repository.get_events_by_tag("bar")

    expected_events = [EVENTS[1], EVENTS[2]]
    assert_same_contents(events, expected_events)


def test_mongo_event_repository__get_events_by_tag_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    with pytest.raises(RetrievalError):
        error_raising_mongo_repository.get_events_by_tag("bar")


def test_mongo_event_repository__get_events_by_source(mongo_repository: IAgentEventRepository):
    source_event = EVENTS[2]
    events = mongo_repository.get_events_by_source(source_event.source)

    expected_events = [source_event]
    assert_same_contents(events, expected_events)


def test_mongo_event_repository__get_events_by_source_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    with pytest.raises(RetrievalError):
        source_event = EVENTS[2]
        error_raising_mongo_repository.get_events_by_source(source_event.source)


def test_mongo_event_repository__reset(mongo_repository: IAgentEventRepository):
    initial_events = mongo_repository.get_events()
    assert initial_events

    mongo_repository.reset()
    events = mongo_repository.get_events()

    assert not events


def test_mongo_event_repository__reset_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    with pytest.raises(RemovalError):
        error_raising_mongo_repository.reset()

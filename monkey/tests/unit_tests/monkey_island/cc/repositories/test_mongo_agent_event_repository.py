import datetime
import uuid
from typing import Any, Iterable, List, Mapping
from unittest.mock import MagicMock

import mongomock
import pytest
from pydantic import Field
from pymongo import MongoClient
from tests.unit_tests.monkey_island.cc.repositories.mongo import get_all_collections_in_mongo

from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    PydanticAgentEventSerializer,
)
from common.agent_events import AbstractAgentEvent
from monkey_island.cc.repositories import (
    IAgentEventRepository,
    MongoAgentEventRepository,
    RemovalError,
    RetrievalError,
    StorageError,
)
from monkey_island.cc.repositories.agent_event_encryption import (
    ENCRYPTED_PREFIX,
    SERIALIZED_EVENT_FIELDS,
)
from monkey_island.cc.repositories.consts import MONGO_OBJECT_ID_KEY


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
def mongo_repository(
    mongo_client, event_serializer_registry, repository_encryptor
) -> IAgentEventRepository:
    return MongoAgentEventRepository(mongo_client, event_serializer_registry, repository_encryptor)


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
    error_raising_mongo_client, event_serializer_registry, repository_encryptor
) -> IAgentEventRepository:
    return MongoAgentEventRepository(
        error_raising_mongo_client, event_serializer_registry, repository_encryptor
    )


def assert_same_contents(a, b):
    assert len(a) == len(b)
    for item in a:
        assert item in b


def test_mongo_agent_event_repository__save_event(mongo_repository: IAgentEventRepository):
    event = FakeAgentEvent(source=uuid.uuid4())
    mongo_repository.save_event(event)
    events = mongo_repository.get_events()

    assert event in events


def test_mongo_agent_event_repository__saved_events_are_encrypted(
    mongo_repository: IAgentEventRepository, mongo_client
):
    event = FakeAgentEvent(source=uuid.uuid4())
    mongo_repository.save_event(event)

    assert_events_are_encrypted(mongo_client, [event])


def test_mongo_agent_event_repository__save_event_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    event = FakeAgentEvent(source=uuid.uuid4())

    with pytest.raises(StorageError):
        error_raising_mongo_repository.save_event(event)


def test_mongo_agent_event_repository__get_events(mongo_repository: IAgentEventRepository):
    events = mongo_repository.get_events()

    assert_same_contents(events, EVENTS)


def test_mongo_agent_event_repository__query_events_sorted_by_timestamp(
    mongo_repository: IAgentEventRepository, mongo_client
):
    event_1 = FakeAgentEvent(
        source=uuid.uuid4(), timestamp=datetime.datetime(2000, 1, 1, 12, 0, 0, 0).timestamp()
    )
    event_2 = FakeAgentEvent(
        source=uuid.uuid4(), timestamp=datetime.datetime(2010, 1, 1, 12, 0, 0, 0).timestamp()
    )
    event_3 = FakeAgentEvent(
        source=uuid.uuid4(), timestamp=datetime.datetime(2020, 1, 1, 12, 0, 0, 0).timestamp()
    )
    event_4 = FakeAgentEvent(
        source=uuid.uuid4(), timestamp=datetime.datetime(2030, 1, 1, 12, 0, 0, 0).timestamp()
    )

    mongo_repository.save_event(event_4)
    mongo_repository.save_event(event_2)
    mongo_repository.save_event(event_1)
    mongo_repository.save_event(event_3)

    events = mongo_repository.get_events()
    sorted_events = sorted(events, key=lambda event: event.timestamp)

    assert events == sorted_events


def test_mongo_agent_event_repository__get_events_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    with pytest.raises(RetrievalError):
        error_raising_mongo_repository.get_events()


def test_mongo_agent_event_repository__get_events_by_type(mongo_repository: IAgentEventRepository):
    events = mongo_repository.get_events_by_type(FakeAgentItemEvent)

    expected_events = [EVENTS[3]]
    assert_same_contents(events, expected_events)


def test_mongo_agent_event_repository__get_events_by_type_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    with pytest.raises(RetrievalError):
        error_raising_mongo_repository.get_events_by_type(FakeAgentItemEvent)


def test_mongo_agent_event_repository__get_events_by_tag(mongo_repository: IAgentEventRepository):
    events = mongo_repository.get_events_by_tag("bar")

    expected_events = [EVENTS[1], EVENTS[2]]
    assert_same_contents(events, expected_events)


def test_mongo_agent_event_repository__get_events_by_tag_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    with pytest.raises(RetrievalError):
        error_raising_mongo_repository.get_events_by_tag("bar")


def test_mongo_agent_event_repository__get_events_by_source(
    mongo_repository: IAgentEventRepository,
):
    source_event = EVENTS[2]
    events = mongo_repository.get_events_by_source(source_event.source)

    expected_events = [source_event]
    assert_same_contents(events, expected_events)


def test_mongo_agent_event_repository__get_events_by_source_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    with pytest.raises(RetrievalError):
        source_event = EVENTS[2]
        error_raising_mongo_repository.get_events_by_source(source_event.source)


def test_mongo_agent_event_repository__reset(mongo_repository: IAgentEventRepository):
    initial_events = mongo_repository.get_events()
    assert initial_events

    mongo_repository.reset()
    events = mongo_repository.get_events()

    assert not events


def test_mongo_agent_event_repository__reset_raises(
    error_raising_mongo_repository: IAgentEventRepository,
):
    with pytest.raises(RemovalError):
        error_raising_mongo_repository.reset()


def get_all_events_in_mongo(
    mongo_client: MongoClient,
) -> Iterable[Mapping[str, Mapping[str, Any]]]:
    events = []

    for collection in get_all_collections_in_mongo(mongo_client):
        mongo_events = collection.find({}, {MONGO_OBJECT_ID_KEY: False})
        for mongo_event in mongo_events:
            events.append(mongo_event)

    return events


def is_encrypted_event(original_event: AbstractAgentEvent, other_event) -> bool:
    """
    Checks if an event is an encrypted version of the original

    - The number of fields match
    - The AbstractAgentEvent fields match
    - The remaining fields have a matching encrypted_ prefix
    - The remaining fields are the encrypted version of the original fields
    """

    event = original_event.dict(simplify=True)

    # Note: The serializer adds a "type" field
    event["type"] = type(original_event).__name__

    if len(event.keys()) != len(other_event.keys()):
        return False

    for field in event.keys():
        if field in SERIALIZED_EVENT_FIELDS:
            if event[field] != other_event[field]:
                return False
        else:
            encrypted_field = ENCRYPTED_PREFIX + field
            if (
                encrypted_field not in other_event.keys()
                or event[field] == other_event[encrypted_field]
            ):
                return False

    return True


def assert_events_are_encrypted(
    mongo_client: MongoClient, original_events: Iterable[AbstractAgentEvent]
):
    stored_events = get_all_events_in_mongo(mongo_client)

    for event in original_events:
        assert any([is_encrypted_event(event, se) for se in stored_events])

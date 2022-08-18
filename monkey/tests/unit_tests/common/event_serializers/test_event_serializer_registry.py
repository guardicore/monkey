from dataclasses import dataclass, field
from unittest.mock import MagicMock

import pytest

from common.event_serializers import EventSerializerRegistry, IEventSerializer
from common.events import AbstractEvent


@dataclass(frozen=True)
class SomeEvent(AbstractEvent):
    some_param: int = field(default=435)


@dataclass(frozen=True)
class OtherEvent(AbstractEvent):
    other_param: float = field(default=123.456)


@dataclass(frozen=True)
class NoneEvent(AbstractEvent):
    none_param: float = field(default=1.0)


SOME_SERIALIZER = MagicMock(spec=IEventSerializer)
OTHER_SERIALIZER = MagicMock(spec=IEventSerializer)


@pytest.fixture
def event_serializer_registry():
    event_serializer_registry = EventSerializerRegistry()

    event_serializer_registry[SomeEvent] = SOME_SERIALIZER
    event_serializer_registry[OtherEvent] = OTHER_SERIALIZER

    return event_serializer_registry


def test_event_serializer_registry_event(event_serializer_registry):
    assert event_serializer_registry[SomeEvent] == SOME_SERIALIZER
    assert event_serializer_registry[OtherEvent] == OTHER_SERIALIZER


def test_event_serializer_registry_string(event_serializer_registry):
    assert event_serializer_registry[SomeEvent.__name__] == SOME_SERIALIZER
    assert event_serializer_registry[OtherEvent.__name__] == OTHER_SERIALIZER


def test_event_serializer_registry_set_unsupported_type(event_serializer_registry):
    with pytest.raises(TypeError):
        event_serializer_registry[SomeEvent] = "SomethingBogusVogus"


def test_event_serializer_registry_set_unsupported_type_key(event_serializer_registry):
    with pytest.raises(TypeError):
        event_serializer_registry["BogusKey"] = MagicMock(spec=IEventSerializer)


def test_event_serializer_registry_get_unsuported_type(event_serializer_registry):
    with pytest.raises(TypeError):
        event_serializer_registry[1]


def test_event_serializer_registry_get_unexisting_type(event_serializer_registry):
    with pytest.raises(KeyError):
        event_serializer_registry[NoneEvent]


def test_event_serializer_registry_get_unexisting_string(event_serializer_registry):
    with pytest.raises(KeyError):
        event_serializer_registry[NoneEvent.__name__]

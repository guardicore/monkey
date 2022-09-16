from unittest.mock import MagicMock

import pytest
from pydantic import Field

from common.agent_event_serializers import AgentEventSerializerRegistry, IAgentEventSerializer
from common.events import AbstractAgentEvent


class SomeEvent(AbstractAgentEvent):
    some_param: int = Field(default=435)


class OtherEvent(AbstractAgentEvent):
    other_param: float = Field(default=123.456)


class NoneEvent(AbstractAgentEvent):
    none_param: float = Field(default=1.0)


SOME_SERIALIZER = MagicMock(spec=IAgentEventSerializer)
OTHER_SERIALIZER = MagicMock(spec=IAgentEventSerializer)


@pytest.fixture
def event_serializer_registry():
    event_serializer_registry = AgentEventSerializerRegistry()

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
        event_serializer_registry["BogusKey"] = MagicMock(spec=IAgentEventSerializer)


def test_event_serializer_registry_get_unsuported_type(event_serializer_registry):
    with pytest.raises(TypeError):
        event_serializer_registry[1]


def test_event_serializer_registry_get_unexisting_type(event_serializer_registry):
    with pytest.raises(KeyError):
        event_serializer_registry[NoneEvent]


def test_event_serializer_registry_get_unexisting_string(event_serializer_registry):
    with pytest.raises(KeyError):
        event_serializer_registry[NoneEvent.__name__]

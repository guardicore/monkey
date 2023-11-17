from unittest.mock import MagicMock

import pytest
from monkeyevents import AbstractAgentEvent, IAgentEventSerializer
from pydantic import Field

from common.agent_event_serializers import AgentEventSerializerRegistry


class SomeEvent(AbstractAgentEvent):
    some_param: int = Field(default=435)


class OtherEvent(AbstractAgentEvent):
    other_param: float = Field(default=123.456)


class NoneEvent(AbstractAgentEvent):
    none_param: float = Field(default=1.0)


SOME_SERIALIZER = MagicMock(spec=IAgentEventSerializer)
OTHER_SERIALIZER = MagicMock(spec=IAgentEventSerializer)


@pytest.fixture
def agent_event_serializer_registry():
    agent_event_serializer_registry = AgentEventSerializerRegistry()

    agent_event_serializer_registry[SomeEvent] = SOME_SERIALIZER
    agent_event_serializer_registry[OtherEvent] = OTHER_SERIALIZER

    return agent_event_serializer_registry


def test_agent_event_serializer_registry_event(agent_event_serializer_registry):
    assert agent_event_serializer_registry[SomeEvent] == SOME_SERIALIZER
    assert agent_event_serializer_registry[OtherEvent] == OTHER_SERIALIZER


def test_agent_event_serializer_registry_string(agent_event_serializer_registry):
    assert agent_event_serializer_registry[SomeEvent.__name__] == SOME_SERIALIZER
    assert agent_event_serializer_registry[OtherEvent.__name__] == OTHER_SERIALIZER


def test_agent_event_serializer_registry_set_unsupported_type(agent_event_serializer_registry):
    with pytest.raises(TypeError):
        agent_event_serializer_registry[SomeEvent] = "SomethingBogusVogus"


def test_agent_event_serializer_registry_set_unsupported_type_key(agent_event_serializer_registry):
    with pytest.raises(TypeError):
        agent_event_serializer_registry["BogusKey"] = MagicMock(spec=IAgentEventSerializer)


def test_agent_event_serializer_registry_get_unsuported_type(agent_event_serializer_registry):
    with pytest.raises(TypeError):
        agent_event_serializer_registry[1]


def test_agent_event_serializer_registry_get_unexisting_type(agent_event_serializer_registry):
    with pytest.raises(KeyError):
        agent_event_serializer_registry[NoneEvent]


def test_agent_event_serializer_registry_get_unexisting_string(agent_event_serializer_registry):
    with pytest.raises(KeyError):
        agent_event_serializer_registry[NoneEvent.__name__]

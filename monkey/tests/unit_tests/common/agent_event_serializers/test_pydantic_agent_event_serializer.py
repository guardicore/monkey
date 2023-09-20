from abc import ABC
from dataclasses import dataclass
from uuid import UUID

import pytest
from pydantic import Field

from common.agent_event_serializers import (
    EVENT_TYPE_FIELD,
    IAgentEventSerializer,
    PydanticAgentEventSerializer,
)
from common.agent_events import AbstractAgentEvent

AGENT_ID = UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5")


@dataclass(frozen=True)
class NotAgentEvent(ABC):
    some_field: int
    other_field: float


class SomeAgentEvent(AbstractAgentEvent):
    bogus: int = Field(default_factory=int)


class PydanticEvent(AbstractAgentEvent):
    some_field: str


@pytest.fixture
def pydantic_agent_event_serializer() -> IAgentEventSerializer:
    return PydanticAgentEventSerializer(PydanticEvent)


@pytest.mark.parametrize(
    "event",
    [NotAgentEvent(some_field=1, other_field=2.0), SomeAgentEvent(source=AGENT_ID, bogus=2)],
)
def test_pydantic_agent_event_serializer__serialize_wrong_type(
    pydantic_agent_event_serializer, event
):
    with pytest.raises(TypeError):
        pydantic_agent_event_serializer.serialize(event)


def test_pydantic_agent_event_serializer__deserialize_wrong_type(pydantic_agent_event_serializer):
    with pytest.raises(TypeError):
        pydantic_agent_event_serializer.deserialize("bla")


def test_pydantic_agent_event_serializer__deserialize(pydantic_agent_event_serializer):
    pydantic_event = PydanticEvent(source=AGENT_ID, some_field="some_field")

    serialized_event = pydantic_agent_event_serializer.serialize(pydantic_event)
    deserialized_object = pydantic_agent_event_serializer.deserialize(serialized_event)

    assert type(serialized_event) != type(deserialized_object)  # noqa: E721
    assert deserialized_object == pydantic_event


def test_pydantic_event_serializer__serialize_inclued_type(pydantic_agent_event_serializer):
    pydantic_event = PydanticEvent(source=AGENT_ID, some_field="some_field")

    serialized_event = pydantic_agent_event_serializer.serialize(pydantic_event)
    assert serialized_event[EVENT_TYPE_FIELD] == PydanticEvent.__name__

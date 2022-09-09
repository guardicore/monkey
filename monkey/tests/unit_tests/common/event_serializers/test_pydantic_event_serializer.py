from abc import ABC
from dataclasses import dataclass, field

import pytest
from pydantic import ValidationError

from common.base_models import InfectionMonkeyBaseModel
from common.event_serializers import PydanticEventSerializer
from common.events import AbstractAgentEvent


@dataclass(frozen=True)
class NotAgentEvent(ABC):
    some_field: int
    other_field: float


@dataclass(frozen=True)
class SomeAgentEvent(AbstractAgentEvent):
    bogus: int = field(default_factory=int)


class PydanticEvent(InfectionMonkeyBaseModel):
    some_field: str


@pytest.fixture
def pydantic_event_serializer():
    return PydanticEventSerializer(PydanticEvent)


@pytest.mark.parametrize("event", [NotAgentEvent(1, 2.0), SomeAgentEvent(2)])
def test_pydantic_event_serializer__serialize_wrong_type(pydantic_event_serializer, event):
    with pytest.raises(TypeError):
        pydantic_event_serializer.serialize(event)


def test_pydantic_event_serializer__deserialize_wrong_type(pydantic_event_serializer):
    with pytest.raises(ValidationError):
        pydantic_event_serializer.deserialize("bla")


def test_pydanitc_event_serializer__de_serialize(pydantic_event_serializer):
    pydantic_event = PydanticEvent(some_field="some_field")

    serialized_event = pydantic_event_serializer.serialize(pydantic_event)
    deserialized_object = pydantic_event_serializer.deserialize(serialized_event)

    assert type(serialized_event) != type(deserialized_object)
    assert deserialized_object == pydantic_event

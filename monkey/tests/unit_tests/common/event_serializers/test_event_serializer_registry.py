from dataclasses import dataclass, field

from common.event_serializers import EventSerializerRegistry
from common.events import AbstractEvent


@dataclass(frozen=True)
class SomeEvent(AbstractEvent):
    some_param: int = field(default=435)


@dataclass(frozen=True)
class OtherEvent(AbstractEvent):
    other_param: float = field(default=123.456)


def test_event_serializer_registry():

    event_serializer_registry = EventSerializerRegistry()

    some_event = SomeEvent(some_param=123)
    other_event = OtherEvent()

    event_serializer_registry[SomeEvent] = some_event
    event_serializer_registry[OtherEvent] = other_event

    assert event_serializer_registry[some_event.__class__] == some_event
    assert event_serializer_registry[other_event.__class__] == other_event

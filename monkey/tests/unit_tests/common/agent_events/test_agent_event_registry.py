import pytest
from monkeyevents import AbstractAgentEvent
from pydantic import Field

from common.agent_events import AgentEventRegistry


def test_reject_invalid_classes():
    class T:
        pass

    registry = AgentEventRegistry()

    with pytest.raises(TypeError):
        registry.register(T)


def test_registration():
    class SomeEvent(AbstractAgentEvent):
        some_param: int = Field(default=435)

    class OtherEvent(AbstractAgentEvent):
        other_param: float = Field(default=123.456)

    registry = AgentEventRegistry()

    registry.register(SomeEvent)
    registry.register(OtherEvent)

    assert registry[SomeEvent.__name__] == SomeEvent
    assert registry[OtherEvent.__name__] == OtherEvent


def test_key_error():
    registry = AgentEventRegistry()

    with pytest.raises(KeyError):
        registry["Nonexistant"]

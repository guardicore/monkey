from typing import Type

from monkeyevents import AbstractAgentEvent


class AgentEventRegistry:
    """
    Registry that maps event type names to classes

    Example:
        event_registry = AgentEventSerializerRegistry()
        event_registry.register(MyEvent)

        event_type = event_registry["MyEvent"]
    """

    def __init__(self):
        self._registry = {}

    def register(self, event_type: Type[AbstractAgentEvent]):
        if not issubclass(event_type, AbstractAgentEvent):
            raise TypeError(f"Event class must be of type: {AbstractAgentEvent.__name__}")

        self._registry[event_type.__name__] = event_type

    def __getitem__(self, event_type_name: str) -> Type[AbstractAgentEvent]:
        return self._registry[event_type_name]

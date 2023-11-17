from typing import Type, Union

from monkeyevents import AbstractAgentEvent, IAgentEventSerializer


class AgentEventSerializerRegistry:
    """
    Registry for event serializers using event class.

    Example:
        event_serializer_registry = AgentEventSerializerRegistry()
        event_serializer_registry[MyEvent] = MyEventSerializer()

        my_event_dict = {"type": "MyEvent", "data": "123"}

        serializer = event_serializer_registry[my_event_dict["type"]]
        my_event_object = serializer.deserialize(my_event_dict)
    """

    def __init__(self):
        self._registry = {}

    def __setitem__(
        self, event_class: Type[AbstractAgentEvent], event_serializer: IAgentEventSerializer
    ):
        if not issubclass(event_class, AbstractAgentEvent):
            raise TypeError(f"Event class must be of type: {AbstractAgentEvent.__name__}")

        if not isinstance(event_serializer, IAgentEventSerializer):
            raise TypeError(f"Event serializer must be of type: {IAgentEventSerializer.__name__}")

        self._registry[event_class] = event_serializer
        self._registry[event_class.__name__] = event_serializer

    def __getitem__(
        self, event_class: Union[str, Type[AbstractAgentEvent]]
    ) -> IAgentEventSerializer:
        if not (isinstance(event_class, str) or issubclass(event_class, AbstractAgentEvent)):
            raise TypeError(
                f"Registry get key {event_class} must be of type: {AbstractAgentEvent.__name__} or "
                f"{str.__name__}"
            )

        return self._registry[event_class]

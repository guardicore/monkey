from typing import Type, Union

from common.event_serializers import IEventSerializer
from common.events import AbstractEvent


class EventSerializerRegistry:
    """
    Registry for event serializers using event class.

    Example:
        event_serializer_registry = EventSerializerRegistry()
        event_serializer_registry[MyEvent] = MyEventSerializer()

        my_event_dict = {"type": "MyEvent", "data": "123"}

        serializer = event_serializer_registry[my_event_dict["type"]]
        my_event_object = serializer.deserialize(my_event_dict)
    """

    def __init__(self):
        self._registry = {}

    def __setitem__(self, event_class: Type[AbstractEvent], event_serializer: IEventSerializer):
        if not issubclass(event_class, AbstractEvent):
            raise TypeError(f"Event class must be of type: {AbstractEvent.__name__}")

        if not isinstance(event_serializer, IEventSerializer):
            raise TypeError(f"Event serializer must be of type: {IEventSerializer.__name__}")

        self._registry[event_class] = event_serializer
        self._registry[event_class.__name__] = event_serializer

    def __getitem__(self, event_class: Union[str, Type[AbstractEvent]]) -> IEventSerializer:
        if not (isinstance(event_class, str) or issubclass(event_class, AbstractEvent)):
            raise TypeError(
                f"Registry get key {event_class} must be of type: {AbstractEvent.__name__} or "
                f"{str.__name__}"
            )

        return self._registry[event_class]

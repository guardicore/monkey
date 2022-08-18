from typing import Type, Union

from common.event_serializers import IEventSerializer
from common.events import AbstractEvent


class EventSerializerRegistry:
    """
    Registry for event serializers using event class.
    """

    def __init__(self):
        self._registry = {}

    def __setitem__(self, event_class: Type[AbstractEvent], event_serializer: IEventSerializer):
        self._registry[event_class] = event_serializer

    def __getitem__(self, event_class: Union[str, Type[AbstractEvent]]):
        return self._registry[event_class]

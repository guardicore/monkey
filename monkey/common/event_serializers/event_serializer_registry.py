from common.event_serializers import IEventSerializer


class EventSerializerRegistry:
    """
    Registry for event serializers
    """

    def __init__(self):
        self._registry = {}

    def __setitem__(self, event_class_name: str, event_serializer: IEventSerializer):
        self._registry[event_class_name] = event_serializer

    def __getitem__(self, event_class_name: str):
        event_serializer = self._registry[event_class_name]
        return event_serializer

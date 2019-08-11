from mongoengine import EmbeddedDocument, DateTimeField, StringField

EVENT_TYPES = ("monkey_local_action", "monkey_network_action", "island_action")


class Event(EmbeddedDocument):
    timestamp = DateTimeField(required=True)
    title = StringField(required=True)
    message = StringField()
    event_type = StringField(required=True, choices=EVENT_TYPES)

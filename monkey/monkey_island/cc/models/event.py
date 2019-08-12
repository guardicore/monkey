from datetime import datetime

from mongoengine import EmbeddedDocument, DateTimeField, StringField

from common.data.zero_trust_consts import EVENT_TYPES


class Event(EmbeddedDocument):
    timestamp = DateTimeField(required=True)
    title = StringField(required=True)
    message = StringField()
    event_type = StringField(required=True, choices=EVENT_TYPES)

    @staticmethod
    def create_event(title, message, event_type):
        event = Event(
            timestamp=datetime.now(),
            title=title,
            message=message,
            event_type=event_type
        )

        event.validate(clean=True)

        return event

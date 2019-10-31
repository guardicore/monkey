from datetime import datetime

from mongoengine import EmbeddedDocument, DateTimeField, StringField

from common.data.zero_trust_consts import EVENT_TYPES


class Event(EmbeddedDocument):
    """
    This model represents a single event within a Finding (it is an EmbeddedDocument within Finding). It is meant to
    hold a detail of the Finding.

    This class has 2 main section:
        *   The schema section defines the DB fields in the document. This is the data of the object.
        *   The logic section defines complex questions we can ask about a single document which are asked multiple
            times, or complex action we will perform - somewhat like an API.
    """
    # SCHEMA
    timestamp = DateTimeField(required=True)
    title = StringField(required=True)
    message = StringField()
    event_type = StringField(required=True, choices=EVENT_TYPES)

    # LOGIC
    @staticmethod
    def create_event(title, message, event_type, timestamp=datetime.now()):
        event = Event(
            timestamp=timestamp,
            title=title,
            message=message,
            event_type=event_type
        )

        event.validate(clean=True)

        return event

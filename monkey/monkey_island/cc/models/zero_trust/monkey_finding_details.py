from typing import List

from mongoengine import DateTimeField, Document, StringField, EmbeddedDocumentListField

from monkey_island.cc.models.zero_trust.event import Event

class MonkeyFindingDetails(Document):
    """
    This model represents additional information about monkey finding:
    Events
    """

    # SCHEMA
    events = EmbeddedDocumentListField(document_type=Event, required=False)

    # LOGIC
    def add_events(self, events: List[Event]) -> None:
        self.update(push_all__events=events)

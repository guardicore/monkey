from __future__ import annotations
from typing import List

from mongoengine import Document, EmbeddedDocumentListField

from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.subnet_pair import SubnetPair


class MonkeyFindingDetails(Document):
    """
    This model represents additional information about monkey finding:
    Events
    """

    # SCHEMA
    events = EmbeddedDocumentListField(document_type=Event, required=False)
    checked_subnet_pairs = EmbeddedDocumentListField(document_type=SubnetPair, required=False)

    # LOGIC
    def add_events(self, events: List[Event]) -> MonkeyFindingDetails:
        self.update(push_all__events=events)
        return self

    def add_checked_subnet_pair(self, subnet_pair: SubnetPair) -> MonkeyFindingDetails:
        self.update(push__checked_subnet_pairs=subnet_pair)
        return self

    def is_with_subnet_pair(self, subnet_pair: SubnetPair):
        return subnet_pair in self.checked_subnet_pairs

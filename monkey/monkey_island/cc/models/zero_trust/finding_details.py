from datetime import datetime
from typing import List

from mongoengine import DateTimeField, Document, StringField, EmbeddedDocumentListField

import common.common_consts.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.scoutsuite_finding import ScoutsuiteFinding


class FindingDetails(Document):
    """
    This model represents additional information about monkey finding:
    Events if monkey finding
    Scoutsuite findings if scoutsuite finding
    """

    # SCHEMA
    events = EmbeddedDocumentListField(document_type=Event, required=False)
    scoutsuite_findings = EmbeddedDocumentListField(document_type=ScoutsuiteFinding, required=False)

    # LOGIC
    def add_events(self, events: List[Event]) -> None:
        self.update(push_all__events=events)

    def add_scoutsuite_findings(self, scoutsuite_findings: List[ScoutsuiteFinding]) -> None:
        self.update(push_all__scoutsuite_findings=scoutsuite_findings)

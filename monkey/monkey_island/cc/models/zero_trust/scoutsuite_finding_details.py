from typing import List

from mongoengine import DateTimeField, Document, StringField, EmbeddedDocumentListField

from monkey_island.cc.models.zero_trust.scoutsuite_finding import ScoutsuiteFinding


class ScoutsuiteFindingDetails(Document):
    """
    This model represents additional information about monkey finding:
    Events if monkey finding
    Scoutsuite findings if scoutsuite finding
    """

    # SCHEMA
    scoutsuite_findings = EmbeddedDocumentListField(document_type=ScoutsuiteFinding, required=False)

    def add_scoutsuite_findings(self, scoutsuite_findings: List[ScoutsuiteFinding]) -> None:
        self.update(push_all__scoutsuite_findings=scoutsuite_findings)

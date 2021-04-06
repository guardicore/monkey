from mongoengine import Document, EmbeddedDocumentListField

from monkey_island.cc.models.zero_trust.scoutsuite_rule import ScoutSuiteRule


class ScoutSuiteFindingDetails(Document):

    # SCHEMA
    scoutsuite_rules = EmbeddedDocumentListField(document_type=ScoutSuiteRule, required=False)

    def add_rule(self, rule: ScoutSuiteRule) -> None:
        if rule not in self.scoutsuite_rules:
            self.scoutsuite_rules.append(rule)
            self.save()

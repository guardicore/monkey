from mongoengine import LazyReferenceField

from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding_details import MonkeyFindingDetails


class MonkeyFinding(Finding):
    details = LazyReferenceField(MonkeyFindingDetails, required=True)

    @staticmethod
    def save_finding(test: str,
                     status: str,
                     detail_ref: MonkeyFindingDetails) -> Finding:
        monkey_finding = MonkeyFinding(test=test,
                                       status=status,
                                       details=detail_ref)
        monkey_finding.save()
        return monkey_finding

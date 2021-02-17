from __future__ import annotations

from mongoengine import LazyReferenceField

from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding_details import MonkeyFindingDetails


class MonkeyFinding(Finding):
    # We put additional info into a lazy reference field, because this info should be only
    # pulled when explicitly needed due to performance
    details = LazyReferenceField(MonkeyFindingDetails, required=True)

    @staticmethod
    def save_finding(test: str,
                     status: str,
                     detail_ref: MonkeyFindingDetails) -> MonkeyFinding:
        finding = MonkeyFinding(test=test, status=status, details=detail_ref)
        finding.save()
        return finding

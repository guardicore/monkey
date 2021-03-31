from __future__ import annotations

from mongoengine import LazyReferenceField

from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.scoutsuite_finding_details import ScoutSuiteFindingDetails


class ScoutSuiteFinding(Finding):
    # We put additional info into a lazy reference field, because this info should be only
    # pulled when explicitly needed due to performance
    details = LazyReferenceField(ScoutSuiteFindingDetails, required=True)

    @staticmethod
    def save_finding(test: str,
                     status: str,
                     detail_ref: ScoutSuiteFindingDetails) -> ScoutSuiteFinding:
        finding = ScoutSuiteFinding(test=test, status=status, details=detail_ref)
        finding.save()
        return finding

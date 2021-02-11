from mongoengine import LazyReferenceField

from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.scoutsuite_finding_details import ScoutSuiteFindingDetails


class ScoutSuiteFinding(Finding):
    details = LazyReferenceField(ScoutSuiteFindingDetails, required=True)

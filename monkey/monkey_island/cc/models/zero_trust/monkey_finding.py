from mongoengine import LazyReferenceField

from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding_details import MonkeyFindingDetails


class MonkeyFinding(Finding):
    details = LazyReferenceField(MonkeyFindingDetails, required=True)

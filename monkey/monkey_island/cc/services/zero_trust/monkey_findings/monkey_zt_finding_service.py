from typing import List

from bson import ObjectId

# TODO: Switch to threading.lock and test. Calling gevent.patch_all() is supposed to monkeypatch
#       threading to be compatible with gevent/greenlets.
from gevent.lock import BoundedSemaphore

from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.monkey_finding import MonkeyFinding
from monkey_island.cc.models.zero_trust.monkey_finding_details import MonkeyFindingDetails


class MonkeyZTFindingService:

    # Required to synchronize db state between different threads
    _finding_lock = BoundedSemaphore()

    @staticmethod
    def create_or_add_to_existing(test: str, status: str, events: List[Event]):
        """
        Create a new finding or add the events to an existing one if it's the \
        same (same meaning same status and same test). \

        :raises: Assertion error if this is used when there's more then one \
        finding which fits the query - this is not when this function should be used.
        """
        with MonkeyZTFindingService._finding_lock:
            existing_findings = list(MonkeyFinding.objects(test=test, status=status))
            assert len(existing_findings) < 2, "More than one finding exists for {}:{}".format(
                test, status
            )

            if len(existing_findings) == 0:
                MonkeyZTFindingService.create_new_finding(test, status, events)
            else:
                # Now we know for sure this is the only one
                MonkeyZTFindingService.add_events(existing_findings[0], events)

    @staticmethod
    def create_new_finding(test: str, status: str, events: List[Event]):
        details = MonkeyFindingDetails()
        details.events = events
        details.save()
        MonkeyFinding.save_finding(test, status, details)

    @staticmethod
    def add_events(finding: MonkeyFinding, events: List[Event]):
        finding.details.fetch().add_events(events).save()

    @staticmethod
    def get_events_by_finding(finding_id: str) -> List[object]:
        finding = MonkeyFinding.objects.get(id=finding_id)
        pipeline = [
            {"$match": {"_id": ObjectId(finding.details.id)}},
            {"$unwind": "$events"},
            {"$project": {"events": "$events"}},
            {"$replaceRoot": {"newRoot": "$events"}},
        ]
        return list(MonkeyFindingDetails.objects.aggregate(*pipeline))

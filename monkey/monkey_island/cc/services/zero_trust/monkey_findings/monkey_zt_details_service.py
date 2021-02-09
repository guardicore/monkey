from typing import List

from bson import ObjectId

from common.utils.exceptions import FindingWithoutDetailsError
from monkey_island.cc.models.zero_trust.monkey_finding_details import MonkeyFindingDetails


# How many events of a single finding to return to UI.
# 100 will return 50 latest and 50 oldest events from a finding
MAX_EVENT_FETCH_CNT = 100


class MonkeyZTDetailsService:

    @staticmethod
    def fetch_details_for_display(finding_id: ObjectId) -> dict:
        pipeline = [{'$match': {'_id': finding_id}},
                    {'$addFields': {'oldest_events': {'$slice': ['$events', int(MAX_EVENT_FETCH_CNT / 2)]},
                                    'latest_events': {'$slice': ['$events', int(-1 * MAX_EVENT_FETCH_CNT / 2)]},
                                    'event_count': {'$size': '$events'}}},
                    {'$unset': ['events']}]
        details = list(MonkeyFindingDetails.objects.aggregate(*pipeline))[0]
        if details:
            details['latest_events'] = MonkeyZTDetailsService._remove_redundant_events(details['event_count'],
                                                                                       details['latest_events'])
            return details
        else:
            raise FindingWithoutDetailsError(f"Finding {finding_id} had no details.")

    @staticmethod
    def _remove_redundant_events(fetched_event_count: int, latest_events: List[object]) -> List[object]:
        overlap_count = fetched_event_count - int(MAX_EVENT_FETCH_CNT/2)
        # None of 'latest_events' are in 'oldest_events'
        if overlap_count >= MAX_EVENT_FETCH_CNT:
            return latest_events
        # All 'latest_events' are already in 'oldest_events'
        elif overlap_count <= 0:
            return []
        # Some of 'latest_events' are already in 'oldest_events'.
        # Return only those that are not
        else:
            return latest_events[-1 * overlap_count:]

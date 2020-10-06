from typing import List

from bson import ObjectId

from monkey_island.cc.models.zero_trust.monkey_finding_details import \
    MonkeyFindingDetails

# How many events of a single finding to return to UI.
# 50 will return 50 latest and 50 oldest events from a finding
EVENT_FETCH_CNT = 50


class EventsService:

    @staticmethod
    def fetch_events_for_display(finding_id: ObjectId):
        pipeline = [{'$match': {'_id': finding_id}},
                    {'$addFields': {'oldest_events': {'$slice': ['$events', EVENT_FETCH_CNT]},
                                    'latest_events': {'$slice': ['$events', -1 * EVENT_FETCH_CNT]},
                                    'event_count': {'$size': '$events'}}},
                    {'$unset': ['events']}]
        details = list(MonkeyFindingDetails.objects.aggregate(*pipeline))
        if details:
            details = details[0]
            details['latest_events'] = EventsService._get_events_without_overlap(details['event_count'],
                                                                                 details['latest_events'])
        return details

    @staticmethod
    def _get_events_without_overlap(event_count: int, events: List[object]) -> List[object]:
        overlap_count = event_count - EVENT_FETCH_CNT
        if overlap_count >= EVENT_FETCH_CNT:
            return events
        elif overlap_count <= 0:
            return []
        else:
            return events[-1 * overlap_count:]

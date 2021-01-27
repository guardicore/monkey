from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.monkey_finding_details import MonkeyFindingDetails

EVENTS = [
    {
        "timestamp": "2021-01-20T15:40:28.357Z",
        "title": "Process list",
        "message": "Monkey on gc-pc-244 scanned the process list",
        "event_type": "monkey_local"
    },
    {
        "timestamp": "2021-01-20T16:08:29.519Z",
        "title": "Process list",
        "message": "",
        "event_type": "monkey_local"
    },
]

EVENTS_DTO = [
    Event(timestamp=event['timestamp'],
          title=event['title'],
          message=event['message'],
          event_type=event['event_type']) for event in EVENTS
]

DETAILS_DTO = []


def get_monkey_details_dto() -> MonkeyFindingDetails:
    monkey_details = MonkeyFindingDetails()
    monkey_details.events.append(EVENTS_DTO[0])
    monkey_details.events.append(EVENTS_DTO[1])
    return monkey_details

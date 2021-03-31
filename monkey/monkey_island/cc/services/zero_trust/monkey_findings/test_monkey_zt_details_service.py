from monkey_island.cc.services.zero_trust.monkey_findings import monkey_zt_details_service
from monkey_island.cc.services.zero_trust.monkey_findings.monkey_zt_details_service import MonkeyZTDetailsService


def test__remove_redundant_events(monkeypatch):
    monkeypatch.setattr(monkey_zt_details_service, 'MAX_EVENT_FETCH_CNT', 6)

    # No events are redundant, 8 events in the database, but we display only 6 (3 latest and 3 oldest)
    latest_events = ['6', '7', '8']
    _do_redundant_event_removal_test(latest_events, 8, ['6', '7', '8'])

    # All latest events are redundant (only 3 events in db and we fetched them twice)
    latest_events = ['1', '2', '3']
    _do_redundant_event_removal_test(latest_events, 3, [])

    # Some latest events are redundant (5 events in db and we fetched 3 oldest and 3 latest)
    latest_events = ['3', '4', '5']
    _do_redundant_event_removal_test(latest_events, 5, ['4', '5'])

    # None of the events are redundant (6 events in db and we fetched 3 oldest and 3 latest)
    latest_events = ['4', '5', '6']
    _do_redundant_event_removal_test(latest_events, 6, ['4', '5', '6'])

    # No events fetched, should return empty array also
    latest_events = []
    _do_redundant_event_removal_test(latest_events, 0, [])


def _do_redundant_event_removal_test(input_list, fetched_event_cnt, expected_output):
    output_events = MonkeyZTDetailsService._remove_redundant_events(fetched_event_cnt, input_list)
    assert output_events == expected_output

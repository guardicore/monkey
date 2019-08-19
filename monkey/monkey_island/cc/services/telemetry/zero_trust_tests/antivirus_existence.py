import json

from common.data.zero_trust_consts import EVENT_TYPE_MONKEY_LOCAL, ANTI_VIRUS_KNOWN_PROCESS_NAMES, EVENT_TYPE_ISLAND, \
    STATUS_POSITIVE, STATUS_CONCLUSIVE, TEST_ENDPOINT_SECURITY_EXISTS
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.event import Event
from monkey_island.cc.models.finding import Finding


def test_antivirus_existence(telemetry_json):
    current_monkey = Monkey.get_single_monkey_by_guid(telemetry_json['monkey_guid'])
    if 'process_list' in telemetry_json['data']:
        process_list_event = Event.create_event(
            title="Process list",
            message="Monkey on {} scanned the process list".format(current_monkey.hostname),
            event_type=EVENT_TYPE_MONKEY_LOCAL)
        events = [process_list_event]

        found_av = False
        all_processes = telemetry_json['data']['process_list'].items()
        for process in all_processes:
            process_name = process[1]['name']
            if process_name in ANTI_VIRUS_KNOWN_PROCESS_NAMES:
                found_av = True
                events.append(Event.create_event(
                    title="Found AV process",
                    message="The process '{}' was recognized as an Anti Virus process. Process "
                            "details: {}".format(process_name, json.dumps(process[1])),
                    event_type=EVENT_TYPE_ISLAND
                ))

        if found_av:
            test_status = STATUS_POSITIVE
        else:
            test_status = STATUS_CONCLUSIVE
        Finding.save_finding(test=TEST_ENDPOINT_SECURITY_EXISTS, status=test_status, events=events)
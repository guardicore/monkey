import json

from common.data.zero_trust_consts import EVENT_TYPE_MONKEY_LOCAL, \
    STATUS_PASSED, STATUS_FAILED, TEST_ENDPOINT_SECURITY_EXISTS
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.zero_trust.aggregate_finding import AggregateFinding
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.services.telemetry.zero_trust_tests.known_anti_viruses import ANTI_VIRUS_KNOWN_PROCESS_NAMES


def test_antivirus_existence(telemetry_json):
    current_monkey = Monkey.get_single_monkey_by_guid(telemetry_json['monkey_guid'])
    if 'process_list' in telemetry_json['data']:
        process_list_event = Event.create_event(
            title="Process list",
            message="Monkey on {} scanned the process list".format(current_monkey.hostname),
            event_type=EVENT_TYPE_MONKEY_LOCAL)
        events = [process_list_event]

        av_processes = filter_av_processes(telemetry_json)

        for process in av_processes:
            events.append(Event.create_event(
                title="Found AV process",
                message="The process '{}' was recognized as an Anti Virus process. Process "
                        "details: {}".format(process[1]['name'], json.dumps(process[1])),
                event_type=EVENT_TYPE_MONKEY_LOCAL
            ))

        if len(av_processes) > 0:
            test_status = STATUS_PASSED
        else:
            test_status = STATUS_FAILED
        AggregateFinding.create_or_add_to_existing(
            test=TEST_ENDPOINT_SECURITY_EXISTS, status=test_status, events=events
        )


def filter_av_processes(telemetry_json):
    all_processes = list(telemetry_json['data']['process_list'].items())
    av_processes = []
    for process in all_processes:
        process_name = process[1]['name']
        # This is for case-insensitive `in`. Generator expression is to save memory.
        if process_name.upper() in (known_av_name.upper() for known_av_name in ANTI_VIRUS_KNOWN_PROCESS_NAMES):
            av_processes.append(process)
    return av_processes

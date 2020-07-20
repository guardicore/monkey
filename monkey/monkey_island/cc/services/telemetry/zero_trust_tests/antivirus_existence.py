import json

import common.data.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.zero_trust.aggregate_finding import \
    AggregateFinding
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.services.telemetry.zero_trust_tests.known_anti_viruses import \
    ANTI_VIRUS_KNOWN_PROCESS_NAMES


def test_antivirus_existence(process_list_json, monkey_guid):
    current_monkey = Monkey.get_single_monkey_by_guid(monkey_guid)

    process_list_event = Event.create_event(
        title="Process list",
        message="Monkey on {} scanned the process list".format(current_monkey.hostname),
        event_type=zero_trust_consts.EVENT_TYPE_MONKEY_LOCAL)
    events = [process_list_event]

    av_processes = filter_av_processes(process_list_json["process_list"])

    for process in av_processes:
        events.append(Event.create_event(
            title="Found AV process",
            message="The process '{}' was recognized as an Anti Virus process. Process "
                    "details: {}".format(process[1]['name'], json.dumps(process[1])),
            event_type=zero_trust_consts.EVENT_TYPE_MONKEY_LOCAL
        ))

    if len(av_processes) > 0:
        test_status = zero_trust_consts.STATUS_PASSED
    else:
        test_status = zero_trust_consts.STATUS_FAILED
    AggregateFinding.create_or_add_to_existing(
        test=zero_trust_consts.TEST_ENDPOINT_SECURITY_EXISTS, status=test_status, events=events
    )


def filter_av_processes(process_list):
    all_processes = list(process_list.items())
    av_processes = []
    for process in all_processes:
        process_name = process[1]['name']
        # This is for case-insensitive `in`. Generator expression is to save memory.
        if process_name.upper() in (known_av_name.upper() for known_av_name in ANTI_VIRUS_KNOWN_PROCESS_NAMES):
            av_processes.append(process)
    return av_processes

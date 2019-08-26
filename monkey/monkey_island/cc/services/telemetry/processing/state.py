from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.telemetry.zero_trust_tests.segmentation import \
    test_positive_findings_for_unreached_segments


def process_state_telemetry(telemetry_json):
    monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])
    NodeService.add_communication_info(monkey, telemetry_json['command_control_channel'])
    if telemetry_json['data']['done']:
        NodeService.set_monkey_dead(monkey, True)
    else:
        NodeService.set_monkey_dead(monkey, False)

    if telemetry_json['data']['done']:
        test_positive_findings_for_unreached_segments(telemetry_json)

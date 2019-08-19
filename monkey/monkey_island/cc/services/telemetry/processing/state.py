from monkey_island.cc.services.node import NodeService


def process_state_telemetry(telemetry_json):
    monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])
    if telemetry_json['data']['done']:
        NodeService.set_monkey_dead(monkey, True)
    else:
        NodeService.set_monkey_dead(monkey, False)

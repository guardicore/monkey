from monkey_island.cc.services.node import NodeService


def process_privilege_escalation_telemetry(telemetry_json):
    NodeService.add_privilege_escalation(telemetry_json)



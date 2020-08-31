from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.telemetry.processing.utils import \
    get_tunnel_host_ip_from_proxy_field
from monkey_island.cc.services.telemetry.zero_trust_tests.tunneling import \
    test_tunneling_violation


def process_tunnel_telemetry(telemetry_json):
    test_tunneling_violation(telemetry_json)
    monkey_id = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])["_id"]
    if telemetry_json['data']['proxy'] is not None:
        tunnel_host_ip = get_tunnel_host_ip_from_proxy_field(telemetry_json)
        NodeService.set_monkey_tunnel(monkey_id, tunnel_host_ip)
    else:
        NodeService.unset_all_monkey_tunnels(monkey_id)

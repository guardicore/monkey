from monkey_island.cc.services.node import NodeService


def process_tunnel_telemetry(telemetry_json):
    monkey_id = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])["_id"]
    if telemetry_json['data']['proxy'] is not None:
        tunnel_host_ip = telemetry_json['data']['proxy'].split(":")[-2].replace("//", "")
        NodeService.set_monkey_tunnel(monkey_id, tunnel_host_ip)
    else:
        NodeService.unset_all_monkey_tunnels(monkey_id)

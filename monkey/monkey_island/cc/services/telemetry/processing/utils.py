from monkey_island.cc.services.edge import EdgeService
from monkey_island.cc.services.node import NodeService


def get_edge_by_scan_or_exploit_telemetry(telemetry_json):
    dst_ip = telemetry_json['data']['machine']['ip_addr']
    dst_domain_name = telemetry_json['data']['machine']['domain_name']
    src_monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])
    dst_node = NodeService.get_monkey_by_ip(dst_ip)
    if dst_node is None:
        dst_node = NodeService.get_or_create_node(dst_ip, dst_domain_name)

    return EdgeService.get_or_create_edge(src_monkey["_id"], dst_node["_id"])


def get_tunnel_host_ip_from_proxy_field(telemetry_json):
    tunnel_host_ip = telemetry_json['data']['proxy'].split(":")[-2].replace("//", "")
    return tunnel_host_ip

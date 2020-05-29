import copy
from typing import Dict

from bson import ObjectId
from mongoengine import DoesNotExist

from monkey_island.cc.models.edge import Edge

RIGHT_ARROW = "\u2192"


class EdgeService:

    @staticmethod
    def get_or_create_edge(src_node_id, dst_node_id, src_label, dst_label):
        edge = False
        try:
            edge = Edge.objects.get(src_node_id=src_node_id, dst_node_id=dst_node_id)
        except DoesNotExist:
            edge = Edge(src_node_id=src_node_id, dst_node_id=dst_node_id)
        finally:
            if edge:
                edge.src_label = src_label
                edge.dst_label = dst_label
                edge.save()
        return edge

    @staticmethod
    def update_label(edge: Edge, node_id: ObjectId, label: str):
        if edge.src_node_id == node_id:
            edge.src_label = label
        elif edge.dst_node_id == node_id:
            edge.dst_label = label
        else:
            raise DoesNotExist("Node id provided does not match with any endpoint of an edge provided.")
        edge.save()
        pass

    @staticmethod
    def update_based_on_scan_telemetry(edge: Edge, telemetry: Dict):
        machine_info = copy.deepcopy(telemetry['data']['machine'])
        new_scan = \
            {
                "timestamp": telemetry["timestamp"],
                "data": machine_info
            }
        ip_address = machine_info.pop("ip_addr")
        domain_name = machine_info.pop("domain_name")
        edge.scans.append(new_scan)
        edge.ip_address = ip_address
        edge.domain_name = domain_name
        edge.save()

    @staticmethod
    def update_based_on_exploit(edge: Edge, exploit: Dict):
        edge.exploits.append(exploit)
        edge.save()
        if exploit['result']:
            EdgeService.set_edge_exploited(edge)

    @staticmethod
    def set_edge_exploited(edge: Edge):
        edge.exploited = True
        edge.save()

    @staticmethod
    def get_edge_group(edge: Edge):
        if edge.exploited:
            return "exploited"
        if edge.tunnel:
            return "tunnel"
        if edge.scans or edge.exploits:
            return "scan"
        return "empty"

    @staticmethod
    def get_edge_label(edge):
        return "%s %s %s" % (edge['src_label'], RIGHT_ARROW, edge['dst_label'])

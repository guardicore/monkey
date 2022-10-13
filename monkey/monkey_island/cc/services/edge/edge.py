from __future__ import annotations

import threading
from typing import Dict, List

from bson import ObjectId
from mongoengine import DoesNotExist

from monkey_island.cc.models.edge import Edge

RIGHT_ARROW = "\u2192"

lock = threading.Lock()


class EdgeService(Edge):
    @staticmethod
    def get_all_edges() -> List[EdgeService]:
        return EdgeService.objects()

    @staticmethod
    def get_or_create_edge(src_node_id, dst_node_id, src_label, dst_label) -> EdgeService:
        with lock:
            edge = None
            try:
                edge = EdgeService.objects.get(src_node_id=src_node_id, dst_node_id=dst_node_id)
            except DoesNotExist:
                edge = EdgeService(src_node_id=src_node_id, dst_node_id=dst_node_id)
            finally:
                if edge:
                    edge.update_label(node_id=src_node_id, label=src_label)
                    edge.update_label(node_id=dst_node_id, label=dst_label)
            return edge

    @staticmethod
    def get_by_dst_node(dst_node_id: ObjectId) -> List[EdgeService]:
        return EdgeService.objects(dst_node_id=dst_node_id)

    @staticmethod
    def get_edge_by_id(edge_id: ObjectId) -> EdgeService:
        return EdgeService.objects.get(id=edge_id)

    def update_label(self, node_id: ObjectId, label: str):
        if self.src_node_id == node_id:
            self.src_label = label
        elif self.dst_node_id == node_id:
            self.dst_label = label
        else:
            raise DoesNotExist(
                "Node id provided does not match with any endpoint of an self provided."
            )
        self.save()

    @staticmethod
    def update_all_dst_nodes(old_dst_node_id: ObjectId, new_dst_node_id: ObjectId):
        for edge in EdgeService.objects(dst_node_id=old_dst_node_id):
            edge.dst_node_id = new_dst_node_id
            edge.save()

    @staticmethod
    def get_tunnel_edges_by_src(src_node_id) -> List[EdgeService]:
        try:
            return EdgeService.objects(src_node_id=src_node_id, tunnel=True)
        except DoesNotExist:
            return []

    # TODO it's not entirelly clear why the tunnel is unset in
    #  monkey/monkey_island/cc/services/telemetry/processing/tunnel.py:15
    # Either way this can be done by fetching, modifying and saving
    def disable_tunnel(self):
        self.tunnel = False
        self.save()

    def update_based_on_exploit(self, exploit: Dict):
        self.exploits.append(exploit)
        self.save()
        if exploit["exploitation_result"]:
            self.set_exploited()

    def set_exploited(self):
        self.exploited = True
        self.save()

    def get_group(self) -> str:
        if self.exploited:
            return "exploited"
        if self.tunnel:
            return "tunnel"
        if self.scans or self.exploits:
            return "scan"
        return "empty"

    def get_label(self) -> str:
        return f"{self.src_label} {RIGHT_ARROW} {self.dst_label}"

from __future__ import annotations

import threading
from typing import List

from bson import ObjectId
from mongoengine import DoesNotExist

from monkey_island.cc.models.edge import Edge

lock = threading.Lock()


class EdgeService(Edge):
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

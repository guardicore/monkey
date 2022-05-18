from abc import ABC
from typing import Optional, Sequence

from monkey_island.cc.models.edge import Edge


class IEdgeRepository(ABC):
    def get_all_edges(self):
        pass

    def get_edges(self, src_machine_id: str, dst_machine_id: str) -> Sequence[Edge]:
        pass

    def save_edge(self, edge: Edge):
        pass

    def get_by_dst(self, dst_machine_id: str) -> Sequence[Edge]:
        pass

    # If tunnel is None then it gets all edges, if True/False then gets only
    # tunneling/non-tunneling edges
    def get_by_src(self, src_machine_id: str, tunnel: Optional[bool] = None) -> Sequence[Edge]:
        pass

    def get_by_id(self, edge_id: str) -> Edge:
        pass

    # Scan telemetries might change the label once we know more about the target system
    def set_label(self, edge_id: str, label: str):
        pass

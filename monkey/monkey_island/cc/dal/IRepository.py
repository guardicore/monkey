from abc import ABC
from typing import Any, Optional, Sequence

from monkey_island.cc.models import Config, Monkey
from monkey_island.cc.models.edge import Edge


class IRepository(ABC):

    # Config
    ###############################################

    # This returns the current config
    # TODO investigate if encryption should be here or where
    def get_config(self) -> dict:
        pass

    def set_config(self, config: dict):
        pass

    # Used when only a subset of config is submitted, for example only PBAFiles
    # Used by passing keys, like ['monkey', 'post_breach_actions', 'linux_filename']
    # Using a list is less ambiguous IMO, than using . notation
    def set_config_field(self, key_list: Sequence[str], value: Any):
        pass

    # Used when only a subset of config is needed, for example only PBAFiles
    # Used by passing keys, like ['monkey', 'post_breach_actions', 'linux_filename']
    # Using a list is less ambiguous IMO, than using . notation
    # TODO Still in doubt about encryption, this should probably be determined automatically
    def get_config_field(self, key_list: Sequence[str]) -> Any:
        pass

    # Edges
    ###############################################

    def get_all_edges(self):
        pass

    def get_edge(self, src_node_id: str, dst_node_id: str) -> Edge:
        pass

    def save_edge(self, edge: Edge):
        pass

    def get_by_dst_node(self, dst_node_id: str) -> Sequence[Edge]:
        pass

    # If tunnel is None then it gets all edges, if True/False then gets only
    # tunneling/non-tunneling edges
    def get_by_src_node(self, src_node_id: str, tunnel: Optional[bool] = None) -> Sequence[Edge]:
        pass

    def get_by_id(self, edge_id: str) -> Edge:
        pass

    # Scan telemetries might change the label once we know more about the target system
    def set_label(self, edge_id: str, label: str):
        pass

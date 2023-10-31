from typing import Sequence

from monkeytypes import MachineID

from monkey_island.cc.models import CommunicationType, Node, TCPConnections
from monkey_island.cc.repositories import INodeRepository


class InMemoryNodeRepository(INodeRepository):
    def __init__(self, nodes: Sequence[Node]):
        self._nodes = nodes

    def upsert_communication(
        self, src: MachineID, dst: MachineID, communication_type: CommunicationType
    ):
        pass

    def upsert_tcp_connections(self, machine_id: MachineID, tcp_connections: TCPConnections):
        pass

    def get_nodes(self) -> Sequence[Node]:
        return self._nodes

    def upsert_node(self, node: Node):
        pass

    def get_node_by_machine_id(self, machine_id: MachineID) -> Node:
        pass

    def reset(self):
        pass

from typing import Dict, FrozenSet, Mapping, Tuple, TypeAlias

from monkeytypes import MutableInfectionMonkeyBaseModel, SocketAddress
from pydantic import Field

from . import CommunicationType, MachineID

NodeConnections: TypeAlias = Mapping[MachineID, FrozenSet[CommunicationType]]
TCPConnections: TypeAlias = Dict[MachineID, Tuple[SocketAddress, ...]]


class Node(MutableInfectionMonkeyBaseModel):
    """
    A network node and its outbound connections/communications

    A node is identified by a MachineID and tracks all outbound communication to other machines on
    the network. This is particularly useful for creating graphs of Infection Monkey's activity
    throughout the network.
    """

    machine_id: MachineID = Field(..., allow_mutation=False)
    """The MachineID of the node (source)"""

    connections: NodeConnections = {}
    """All outbound connections from this node to other machines"""

    tcp_connections: TCPConnections = {}
    """All successfull outbound TCP connections"""

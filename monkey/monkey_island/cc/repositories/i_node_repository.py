from abc import ABC, abstractmethod
from typing import Sequence

from monkeytypes import MachineID

from monkey_island.cc.models import CommunicationType, Node, TCPConnections


class INodeRepository(ABC):
    """A repository used to store and retrieve `Node` objects"""

    @abstractmethod
    def upsert_communication(
        self, src: MachineID, dst: MachineID, communication_type: CommunicationType
    ):
        """
        Insert or update a node connection

        Insert or update data about how network nodes are able to communicate. Nodes are identified
        by MachineID and store information about all outbound connections to other machines. By
        providing a source machine, target machine, and how they communicated, nodes in this
        repository can be created if they don't exist or updated if they do.

        :param src: The machine that the connection or communication originated from
        :param dst: The machine that the src communicated with
        :param communication_type: The way the machines communicated
        :raises StorageError: If an error occurs while attempting to upsert the Node
        """

    @abstractmethod
    def upsert_tcp_connections(self, machine_id: MachineID, tcp_connections: TCPConnections):
        """
        Add TCP connections to Node
        :param machine_id: Machine ID of the Node that made the connections
        :param tcp_connections: TCP connections made by node
        :raises StorageError: If an error occurs while attempting to add connections
        """

    @abstractmethod
    def get_nodes(self) -> Sequence[Node]:
        """
        Return all nodes that are stored in the repository

        :return: All known Nodes
        :raises RetrievalError: If an error occurs while attempting to retrieve the nodes
        """

    @abstractmethod
    def upsert_node(self, node: Node):
        """
        Update or insert Node model into the database
        :param node: Node model to be added to the repository
        :raises StorageError: If something went wrong when upserting the Node
        """

    @abstractmethod
    def get_node_by_machine_id(self, machine_id: MachineID) -> Node:
        """
        Fetches network Node from the database based on Machine id
        :param machine_id: ID of a Machine that Node represents
        :return: network Node that represents the Machine
        :raises UnknownRecordError: If the Node does not exist
        """

    @abstractmethod
    def reset(self):
        """
        Removes all data from the repository

        :raises RemovalError: If an error occurs while attempting to remove all `Nodes` from the
                              repository
        """

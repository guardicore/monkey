from abc import ABC, abstractmethod
from typing import Sequence

from monkey_island.cc.models import CommunicationType, MachineID, Node


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
    def get_nodes(self) -> Sequence[Node]:
        """
        Return all nodes that are stored in the repository

        :return: All known Nodes
        :raises RetrievalError: If an error occurs while attempting to retrieve the nodes
        """

    @abstractmethod
    def reset(self):
        """
        Removes all data from the repository

        :raises RemovalError: If an error occurs while attempting to remove all `Nodes` from the
                              repository
        """

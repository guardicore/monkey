from copy import deepcopy
from typing import Sequence

from pymongo import MongoClient

from monkey_island.cc.models import CommunicationType, MachineID, Node

from ..models.node import TCPConnections
from . import INodeRepository, RemovalError, RetrievalError, StorageError, UnknownRecordError
from .consts import MONGO_OBJECT_ID_KEY

UPSERT_ERROR_MESSAGE = "An error occurred while attempting to upsert a node"
SRC_FIELD_NAME = "machine_id"


class MongoNodeRepository(INodeRepository):
    def __init__(self, mongo_client: MongoClient):
        self._nodes_collection = mongo_client.monkey_island.nodes

    def upsert_communication(
        self, src: MachineID, dst: MachineID, communication_type: CommunicationType
    ):
        try:
            node = self.get_node_by_machine_id(src)
            updated_node = MongoNodeRepository._add_connection_to_node(
                node, dst, communication_type
            )
        except UnknownRecordError:
            updated_node = Node(machine_id=src, connections={dst: frozenset((communication_type,))})
        except Exception as err:
            raise StorageError(f"{UPSERT_ERROR_MESSAGE}: {err}")

        self.upsert_node(updated_node)

    @staticmethod
    def _add_connection_to_node(
        node: Node, dst: MachineID, communication_type: CommunicationType
    ) -> Node:
        connections = dict(deepcopy(node.connections))
        communications = set(connections.get(dst, set()))
        communications.add(communication_type)
        connections[dst] = frozenset(communications)

        new_node = node.model_copy()
        new_node.connections = connections

        return new_node

    def upsert_tcp_connections(self, machine_id: MachineID, tcp_connections: TCPConnections):
        try:
            node = self.get_node_by_machine_id(machine_id)
        except UnknownRecordError:
            node = Node(machine_id=machine_id, connections={})

        for target, connections in tcp_connections.items():
            if target in node.tcp_connections:
                node.tcp_connections[target] = tuple({*node.tcp_connections[target], *connections})
            else:
                node.tcp_connections[target] = connections
        self.upsert_node(node)

    def upsert_node(self, node: Node):
        try:
            result = self._nodes_collection.replace_one(
                {SRC_FIELD_NAME: node.machine_id}, node.to_json_dict(), upsert=True
            )
        except Exception as err:
            raise StorageError(f"{UPSERT_ERROR_MESSAGE}: {err}")

        if result.matched_count == 0 and result.upserted_id is None:
            raise StorageError(
                f'Error inserting node with source ID "{node.machine_id}": Expected to insert 1 '
                f"node, but no nodes were inserted"
            )

    def get_node_by_machine_id(self, machine_id: MachineID) -> Node:
        node_dict = self._nodes_collection.find_one(
            {SRC_FIELD_NAME: machine_id}, {MONGO_OBJECT_ID_KEY: False}
        )
        if not node_dict:
            raise UnknownRecordError(f"Node with machine ID {machine_id}")
        return Node(**node_dict)

    def get_nodes(self) -> Sequence[Node]:
        try:
            cursor = self._nodes_collection.find({}, {MONGO_OBJECT_ID_KEY: False})
            return [Node(**n) for n in cursor]
        except Exception as err:
            raise RetrievalError(f"Error retrieving nodes from the repository: {err}")

    def reset(self):
        try:
            self._nodes_collection.drop()
        except Exception as err:
            raise RemovalError(f"Error resetting the repository: {err}")

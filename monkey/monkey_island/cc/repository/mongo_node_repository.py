from copy import deepcopy
from typing import Sequence

from pymongo import MongoClient

from monkey_island.cc.models import CommunicationType, MachineID, Node

from . import INodeRepository, RemovalError, RetrievalError, StorageError
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
            node_dict = self._nodes_collection.find_one(
                {SRC_FIELD_NAME: src}, {MONGO_OBJECT_ID_KEY: False}
            )
        except Exception as err:
            raise StorageError(f"{UPSERT_ERROR_MESSAGE}: {err}")

        if node_dict is None:
            updated_node = Node(machine_id=src, connections={dst: frozenset((communication_type,))})
        else:
            node = Node(**node_dict)
            updated_node = MongoNodeRepository._add_connection_to_node(
                node, dst, communication_type
            )

        self._upsert_node(updated_node)

    @staticmethod
    def _add_connection_to_node(
        node: Node, dst: MachineID, communication_type: CommunicationType
    ) -> Node:
        connections = dict(deepcopy(node.connections))
        communications = set(connections.get(dst, set()))
        communications.add(communication_type)
        connections[dst] = frozenset(communications)

        new_node = node.copy()
        new_node.connections = connections

        return new_node

    def _upsert_node(self, node: Node):
        try:
            result = self._nodes_collection.replace_one(
                {SRC_FIELD_NAME: node.machine_id}, node.dict(simplify=True), upsert=True
            )
        except Exception as err:
            raise StorageError(f"{UPSERT_ERROR_MESSAGE}: {err}")

        if result.matched_count != 0 and result.modified_count != 1:
            raise StorageError(
                f'Error updating node with source ID "{node.machine_id}": Expected to update 1 '
                f"node, but {result.modified_count} were updated"
            )

        if result.matched_count == 0 and result.upserted_id is None:
            raise StorageError(
                f'Error inserting node with source ID "{node.machine_id}": Expected to insert 1 '
                f"node, but no nodes were inserted"
            )

    def get_nodes(self) -> Sequence[Node]:
        try:
            cursor = self._nodes_collection.find({}, {MONGO_OBJECT_ID_KEY: False})
            return list(map(lambda n: Node(**n), cursor))
        except Exception as err:
            raise RetrievalError(f"Error retrieving nodes from the repository: {err}")

    def reset(self):
        try:
            self._nodes_collection.drop()
        except Exception as err:
            raise RemovalError(f"Error resetting the repository: {err}")

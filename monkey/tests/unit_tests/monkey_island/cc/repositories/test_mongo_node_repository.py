from unittest.mock import MagicMock

import mongomock
import pytest

from common.types import SocketAddress
from monkey_island.cc.models import CommunicationType, Node
from monkey_island.cc.repositories import (
    INodeRepository,
    MongoNodeRepository,
    RemovalError,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)

TARGET_MACHINE_IP = "2.2.2.2"

TCP_CONNECTION_PORT_22 = {3: (SocketAddress(ip=TARGET_MACHINE_IP, port=22),)}
TCP_CONNECTION_PORT_80 = {3: (SocketAddress(ip=TARGET_MACHINE_IP, port=80),)}
ALL_TCP_CONNECTIONS = {
    3: (SocketAddress(ip=TARGET_MACHINE_IP, port=22), SocketAddress(ip=TARGET_MACHINE_IP, port=80))
}

NODES = (
    Node(
        machine_id=1,
        connections={
            2: frozenset((CommunicationType.SCANNED,)),
            3: frozenset((CommunicationType.SCANNED, CommunicationType.EXPLOITED)),
        },
    ),
    Node(
        machine_id=2,
        connections={1: frozenset((CommunicationType.CC,))},
        tcp_connections=TCP_CONNECTION_PORT_22,
    ),
    Node(
        machine_id=3,
        connections={
            1: frozenset((CommunicationType.CC,)),
            4: frozenset((CommunicationType.SCANNED,)),
            5: frozenset((CommunicationType.SCANNED, CommunicationType.EXPLOITED)),
        },
    ),
    Node(machine_id=4, connections={}, tcp_connections=ALL_TCP_CONNECTIONS),
    Node(
        machine_id=5,
        connections={
            2: frozenset((CommunicationType.SCANNED, CommunicationType.EXPLOITED)),
            3: frozenset((CommunicationType.CC,)),
        },
    ),
)


@pytest.fixture
def empty_node_repository() -> INodeRepository:
    return MongoNodeRepository(mongomock.MongoClient())


@pytest.fixture
def mongo_client() -> mongomock.MongoClient:
    client = mongomock.MongoClient()
    client.monkey_island.nodes.insert_many((n.to_json_dict() for n in NODES))
    return client


@pytest.fixture
def node_repository(mongo_client) -> INodeRepository:
    return MongoNodeRepository(mongo_client)


@pytest.fixture
def error_raising_mock_mongo_client() -> mongomock.MongoClient:
    mongo_client = MagicMock(spec=mongomock.MongoClient)
    mongo_client.monkey_island = MagicMock(spec=mongomock.Database)
    mongo_client.monkey_island.nodes = MagicMock(spec=mongomock.Collection)

    mongo_client.monkey_island.nodes.find = MagicMock(side_effect=Exception("some exception"))
    mongo_client.monkey_island.nodes.find_one = MagicMock(side_effect=Exception("some exception"))
    mongo_client.monkey_island.nodes.replace_one = MagicMock(
        side_effect=Exception("some exception")
    )
    mongo_client.monkey_island.nodes.drop = MagicMock(side_effect=Exception("some exception"))

    return mongo_client


@pytest.fixture
def error_raising_node_repository(error_raising_mock_mongo_client) -> INodeRepository:
    return MongoNodeRepository(error_raising_mock_mongo_client)


def test_upsert_communication__empty_repository(empty_node_repository):
    src_machine_id = 1
    dst_machine_id = 2
    expected_node = Node(
        machine_id=src_machine_id,
        connections={dst_machine_id: frozenset((CommunicationType.SCANNED,))},
    )

    empty_node_repository.upsert_communication(
        src_machine_id, dst_machine_id, CommunicationType.SCANNED
    )
    nodes = empty_node_repository.get_nodes()

    assert len(nodes) == 1
    assert nodes[0] == expected_node


def test_upsert_communication__new_node(node_repository):
    src_machine_id = NODES[-1].machine_id + 100
    dst_machine_id = 1
    expected_nodes = NODES + (
        Node(
            machine_id=src_machine_id,
            connections={dst_machine_id: frozenset((CommunicationType.CC,))},
        ),
    )
    node_repository.upsert_communication(src_machine_id, dst_machine_id, CommunicationType.CC)
    nodes = node_repository.get_nodes()

    assert len(nodes) == len(expected_nodes)
    for en in expected_nodes:
        assert en in nodes


def test_upsert_communication__update_existing_connection(node_repository):
    src_machine_id = 1
    dst_machine_id = 2
    expected_node = NODES[0].model_copy(deep=True)
    expected_node.connections[2] = frozenset(
        (*expected_node.connections[2], CommunicationType.EXPLOITED)
    )
    node_repository.upsert_communication(
        src_machine_id, dst_machine_id, CommunicationType.EXPLOITED
    )
    nodes = node_repository.get_nodes()

    for node in nodes:
        if node.machine_id == src_machine_id:
            assert node == expected_node
            break


def test_upsert_communication__update_existing_node_add_connection(node_repository):
    src_machine_id = 2
    dst_machine_id = 5
    expected_node = NODES[1].model_copy(deep=True)
    expected_node.connections[5] = frozenset((CommunicationType.SCANNED,))
    node_repository.upsert_communication(src_machine_id, dst_machine_id, CommunicationType.SCANNED)
    nodes = node_repository.get_nodes()

    for node in nodes:
        if node.machine_id == src_machine_id:
            assert node == expected_node
            break


def test_upsert_communication__find_one_fails(error_raising_node_repository):
    with pytest.raises(StorageError):
        error_raising_node_repository.upsert_communication(1, 2, CommunicationType.SCANNED)


def test_upsert_communication__replace_one_fails(
    error_raising_mock_mongo_client, error_raising_node_repository
):
    error_raising_mock_mongo_client.monkey_island.nodes.find_one = MagicMock(return_value=None)
    with pytest.raises(StorageError):
        error_raising_node_repository.upsert_communication(1, 2, CommunicationType.SCANNED)


def test_upsert_communication__replace_one_insert_fails(
    error_raising_mock_mongo_client, error_raising_node_repository
):
    mock_result = MagicMock()
    mock_result.matched_count = 0
    mock_result.upserted_id = None
    error_raising_mock_mongo_client.monkey_island.nodes.find_one = MagicMock(return_value=None)
    error_raising_mock_mongo_client.monkey_island.nodes.replace_one = MagicMock(
        return_value=mock_result
    )

    with pytest.raises(StorageError):
        error_raising_node_repository.upsert_communication(1, 2, CommunicationType.SCANNED)


def test_get_nodes(node_repository):
    nodes = node_repository.get_nodes()
    assert len(nodes) == len(nodes)
    for n in nodes:
        assert n in NODES


def test_get_nodes__find_fails(error_raising_node_repository):
    with pytest.raises(RetrievalError):
        error_raising_node_repository.get_nodes()


def test_reset(node_repository):
    assert len(node_repository.get_nodes()) > 0

    node_repository.reset()

    assert len(node_repository.get_nodes()) == 0


def test_reset__removal_error(error_raising_node_repository):
    with pytest.raises(RemovalError):
        error_raising_node_repository.reset()


def test_upsert_tcp_connections__empty_connections(node_repository):
    node_repository.upsert_tcp_connections(1, TCP_CONNECTION_PORT_22)
    nodes = node_repository.get_nodes()
    for node in nodes:
        if node.machine_id == 1:
            assert node.tcp_connections == TCP_CONNECTION_PORT_22


def test_upsert_tcp_connections__upsert_new_port(node_repository):
    node_repository.upsert_tcp_connections(2, TCP_CONNECTION_PORT_80)
    nodes = node_repository.get_nodes()
    modified_node = [node for node in nodes if node.machine_id == 2][0]
    assert set(modified_node.tcp_connections) == set(ALL_TCP_CONNECTIONS)
    assert len(modified_node.tcp_connections) == len(ALL_TCP_CONNECTIONS)


def test_upsert_tcp_connections__port_already_present(node_repository):
    node_repository.upsert_tcp_connections(4, TCP_CONNECTION_PORT_80)
    nodes = node_repository.get_nodes()
    modified_node = [node for node in nodes if node.machine_id == 4][0]
    assert set(modified_node.tcp_connections) == set(ALL_TCP_CONNECTIONS)
    assert len(modified_node.tcp_connections) == len(ALL_TCP_CONNECTIONS)


def test_upsert_tcp_connections__node_missing(node_repository):
    node_repository.upsert_tcp_connections(999, TCP_CONNECTION_PORT_80)
    nodes = node_repository.get_nodes()
    modified_node = [node for node in nodes if node.machine_id == 999][0]
    assert set(modified_node.tcp_connections) == set(TCP_CONNECTION_PORT_80)


def test_get_node_by_machine_id(node_repository):
    assert node_repository.get_node_by_machine_id(1) == NODES[0]


def test_get_node_by_machine_id__no_node(node_repository):
    with pytest.raises(UnknownRecordError):
        node_repository.get_node_by_machine_id(999)

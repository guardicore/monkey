from unittest.mock import MagicMock

import mongomock
import pytest

from monkey_island.cc.models import CommunicationType, Node
from monkey_island.cc.repository import (
    INodeRepository,
    MongoNodeRepository,
    RemovalError,
    RetrievalError,
    StorageError,
)

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
    ),
    Node(
        machine_id=3,
        connections={
            1: frozenset((CommunicationType.CC,)),
            4: frozenset((CommunicationType.SCANNED,)),
            5: frozenset((CommunicationType.SCANNED, CommunicationType.EXPLOITED)),
        },
    ),
    Node(
        machine_id=4,
        connections={},
    ),
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
    client.monkey_island.nodes.insert_many((n.dict(simplify=True) for n in NODES))
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
    expected_node = NODES[0].copy(deep=True)
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
    expected_node = NODES[1].copy(deep=True)
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
    error_raising_mock_mongo_client.monkey_island.nodes.find_one = lambda _: None
    with pytest.raises(StorageError):
        error_raising_node_repository.upsert_communication(1, 2, CommunicationType.SCANNED)


def test_upsert_communication__replace_one_matched_without_modify(
    error_raising_mock_mongo_client, error_raising_node_repository
):
    mock_result = MagicMock()
    mock_result.matched_count = 1
    mock_result.modified_count = 0
    error_raising_mock_mongo_client.monkey_island.nodes.find_one = lambda _: None
    error_raising_mock_mongo_client.monkey_island.nodes.replace_one = lambda *_, **__: mock_result

    with pytest.raises(StorageError):
        error_raising_node_repository.upsert_communication(1, 2, CommunicationType.SCANNED)


def test_upsert_communication__replace_one_insert_fails(
    error_raising_mock_mongo_client, error_raising_node_repository
):
    mock_result = MagicMock()
    mock_result.matched_count = 0
    mock_result.upserted_id = None
    error_raising_mock_mongo_client.monkey_island.nodes.find_one = lambda _: None
    error_raising_mock_mongo_client.monkey_island.nodes.replace_one = lambda *_, **__: mock_result

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

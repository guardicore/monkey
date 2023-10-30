from http import HTTPStatus

import pytest
from monkeytypes import SocketAddress
from tests.common import StubDIContainer
from tests.monkey_island import InMemoryNodeRepository

from monkey_island.cc.models import CommunicationType, Node
from monkey_island.cc.repositories import INodeRepository
from monkey_island.cc.resources import Nodes

NODE_CONNECTIONS = {
    6: frozenset((CommunicationType.SCANNED,)),
    7: frozenset((CommunicationType.SCANNED, CommunicationType.EXPLOITED)),
}

TCP_CONNECTIONS = {
    6: tuple((SocketAddress(ip="192.168.1.1", port=80), SocketAddress(ip="192.168.1.1", port=443))),
    7: tuple((SocketAddress(ip="192.168.1.2", port=22),)),
}


NODE_1 = Node(machine_id=1, connections={}, tcp_connections={})
NODE_2 = Node(machine_id=2, connections=NODE_CONNECTIONS, tcp_connections=TCP_CONNECTIONS)
EXPECTED_NODES = [NODE_1, NODE_2]


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()
    container.register_instance(INodeRepository, InMemoryNodeRepository(EXPECTED_NODES))

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_nodes_endpoint__get(flask_client):
    response = flask_client.get(Nodes.urls[0], follow_redirects=True)
    print(response.json)
    ACTUAL_NODES = [Node(**node_data) for node_data in response.json]

    assert ACTUAL_NODES == EXPECTED_NODES
    assert response.status_code == HTTPStatus.OK

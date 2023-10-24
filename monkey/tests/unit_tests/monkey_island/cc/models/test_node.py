from typing import MutableSequence

import pytest
from monkeytypes import IllegalMutationError

from common.types import SocketAddress
from monkey_island.cc.models import CommunicationType, Node


def test_constructor():
    machine_id = 1
    connections = {
        6: frozenset((CommunicationType.SCANNED,)),
        7: frozenset((CommunicationType.SCANNED, CommunicationType.EXPLOITED)),
    }
    tcp_connections = {
        6: tuple(
            (SocketAddress(ip="192.168.1.1", port=80), SocketAddress(ip="192.168.1.1", port=443))
        ),
        7: tuple((SocketAddress(ip="192.168.1.2", port=22),)),
    }
    n = Node(
        machine_id=machine_id,
        connections=connections,
        tcp_connections=tcp_connections,
    )

    assert n.machine_id == machine_id
    assert n.connections == connections
    assert n.tcp_connections == tcp_connections


def test_serialization():
    node_dict = {
        "machine_id": 1,
        "connections": {
            "6": [CommunicationType.CC.value, CommunicationType.SCANNED.value],
            "7": [CommunicationType.EXPLOITED.value, CommunicationType.CC.value],
        },
        "tcp_connections": {
            "6": [{"ip": "192.168.1.1", "port": 80}, {"ip": "192.168.1.1", "port": 443}],
            "7": [{"ip": "192.168.1.2", "port": 22}],
        },
    }

    n = Node(**node_dict)

    serialized_node = n.to_json_dict()

    # NOTE: Comparing these nodes is difficult because sets are not ordered
    assert len(serialized_node) == len(node_dict)
    for key in serialized_node.keys():
        assert key in node_dict

    assert len(serialized_node["connections"]) == len(node_dict["connections"])

    for key, value in serialized_node["connections"].items():
        assert set(value) == set(node_dict["connections"][key])

    assert serialized_node["tcp_connections"] == node_dict["tcp_connections"]


def test_machine_id_immutable():
    n = Node(machine_id=1, connections={})

    with pytest.raises(IllegalMutationError):
        n.machine_id = 2


def test_machine_id__invalid_type():
    with pytest.raises(TypeError):
        Node(machine_id=None, connections={})


def test_machine_id__invalid_value():
    with pytest.raises(ValueError):
        Node(machine_id=-5, connections={})


def test_connections__mutable():
    n = Node(machine_id=1, connections={})

    # Raises exception on failure
    n.connections = {5: [], 7: []}


def test_connections__invalid_machine_id():
    n = Node(machine_id=1, connections={})

    with pytest.raises(ValueError):
        n.connections = {5: [], -5: []}


def test_connections__recursively_immutable():
    n = Node(
        machine_id=1,
        connections={
            6: [CommunicationType.SCANNED],
            7: [CommunicationType.SCANNED, CommunicationType.EXPLOITED],
        },
    )

    for connections in n.connections.values():
        assert not isinstance(connections, MutableSequence)


def test_connections__set_invalid_communications_type():
    connections = {8: [CommunicationType.SCANNED, "invalid_comm_type"]}

    n = Node(machine_id=1, connections={})

    with pytest.raises(ValueError):
        n.connections = connections

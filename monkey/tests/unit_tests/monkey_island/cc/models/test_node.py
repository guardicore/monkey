from typing import MutableSequence

import pytest

from monkey_island.cc.models import CommunicationType, Node


def test_constructor():
    machine_id = 1
    connections = (
        (6, (CommunicationType.SCANNED,)),
        (7, (CommunicationType.SCANNED, CommunicationType.EXPLOITED)),
    )
    n = Node(
        machine_id=1,
        connections=connections,
    )

    assert n.machine_id == machine_id
    assert n.connections == connections


def test_serialization():
    node_dict = {
        "machine_id": 1,
        "connections": [
            [
                6,
                ["cc", "scanned"],
            ],
            [7, ["exploited", "cc_tunnel"]],
        ],
    }
    n = Node(**node_dict)

    assert n.dict(simplify=True) == node_dict


def test_machine_id_immutable():
    n = Node(machine_id=1, connections=[])

    with pytest.raises(TypeError):
        n.machine_id = 2


def test_machine_id__invalid_type():
    with pytest.raises(TypeError):
        Node(machine_id=None, connections=[])


def test_machine_id__invalid_value():
    with pytest.raises(ValueError):
        Node(machine_id=-5, connections=[])


def test_connections__mutable():
    n = Node(machine_id=1, connections=[])

    # Raises exception on failure
    n.connections = [(5, []), (7, [])]


def test_connections__invalid_machine_id():
    n = Node(machine_id=1, connections=[])

    with pytest.raises(ValueError):
        n.connections = [(5, []), (-5, [])]


def test_connections__recursively_immutable():
    n = Node(
        machine_id=1,
        connections=[
            [6, [CommunicationType.SCANNED]],
            [7, [CommunicationType.SCANNED, CommunicationType.EXPLOITED]],
        ],
    )

    assert not isinstance(n.connections, MutableSequence)
    assert not isinstance(n.connections[0], MutableSequence)
    assert not isinstance(n.connections[1], MutableSequence)
    assert not isinstance(n.connections[0][1], MutableSequence)
    assert not isinstance(n.connections[1][1], MutableSequence)


def test_connections__set_invalid_communications_type():
    connections = (
        [
            [8, [CommunicationType.SCANNED, "invalid_comm_type"]],
        ],
    )

    n = Node(machine_id=1, connections=[])

    with pytest.raises(ValueError):
        n.connections = connections

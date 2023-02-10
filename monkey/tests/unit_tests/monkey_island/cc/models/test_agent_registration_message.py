from datetime import datetime, timezone
from ipaddress import IPv4Interface
from typing import MutableSequence, Sequence
from uuid import UUID

import pytest

from common import AgentRegistrationData
from common.types import SocketAddress

AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
PARENT_ID = UUID("0fc9afcb-1902-436b-bd5c-1ad194252484")
SOCKET_ADDRESS = SocketAddress(ip="192.168.1.1", port=5000)

AGENT_REGISTRATION_MESSAGE_OBJECT_DICT = {
    "id": AGENT_ID,
    "machine_hardware_id": 2,
    "start_time": datetime.fromtimestamp(1660848408, tz=timezone.utc),
    "parent_id": PARENT_ID,
    "cc_server": SOCKET_ADDRESS,
    "network_interfaces": [IPv4Interface("10.0.0.1/24"), IPv4Interface("192.168.5.32/16")],
}

AGENT_REGISTRATION_MESSAGE_SIMPLE_DICT = {
    "id": str(AGENT_ID),
    "machine_hardware_id": 2,
    "start_time": "2022-08-18T18:46:48+00:00",
    "parent_id": str(PARENT_ID),
    "cc_server": SOCKET_ADDRESS.dict(simplify=True),
    "network_interfaces": ["10.0.0.1/24", "192.168.5.32/16"],
}


def test_to_dict():
    a = AgentRegistrationData(**AGENT_REGISTRATION_MESSAGE_OBJECT_DICT)
    simple_dict = AGENT_REGISTRATION_MESSAGE_SIMPLE_DICT.copy()

    assert a.dict(simplify=True) == simple_dict


def test_from_serialized():
    from_serialized = AgentRegistrationData(**AGENT_REGISTRATION_MESSAGE_SIMPLE_DICT)
    from_objects = AgentRegistrationData(**AGENT_REGISTRATION_MESSAGE_OBJECT_DICT)

    assert from_serialized == from_objects


@pytest.mark.parametrize(
    "key, value",
    [
        ("id", 1),
        ("machine_hardware_id", "not-an-int"),
        ("start_time", None),
        ("parent_id", 2.1),
        ("cc_server", [1]),
        ("network_interfaces", "not-a-list"),
    ],
)
def test_construct_invalid_field__type_error(key, value):
    invalid_type_dict = AGENT_REGISTRATION_MESSAGE_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(TypeError):
        AgentRegistrationData(**invalid_type_dict)


@pytest.mark.parametrize(
    "key, value",
    [
        ("machine_hardware_id", -1),
        ("start_time", "not-a-date-time"),
        ("network_interfaces", [1, "stuff", 3]),
        ("cc_server", []),
    ],
)
def test_construct_invalid_field__value_error(key, value):
    invalid_value_dict = AGENT_REGISTRATION_MESSAGE_SIMPLE_DICT.copy()
    invalid_value_dict[key] = value

    with pytest.raises(ValueError):
        AgentRegistrationData(**invalid_value_dict)


@pytest.mark.parametrize(
    "key, value",
    [
        ("id", PARENT_ID),
        ("machine_hardware_id", 99),
        ("start_time", 0),
        ("parent_id", AGENT_ID),
        ("cc_server", SOCKET_ADDRESS),
        ("network_interfaces", ["10.0.0.1/24"]),
    ],
)
def test_fields_immutable(key, value):
    a = AgentRegistrationData(**AGENT_REGISTRATION_MESSAGE_OBJECT_DICT)

    with pytest.raises(TypeError):
        setattr(a, key, value)


def test_network_interfaces_sequence_immutable():
    a = AgentRegistrationData(**AGENT_REGISTRATION_MESSAGE_OBJECT_DICT)

    assert isinstance(a.network_interfaces, Sequence)
    assert not isinstance(a.network_interfaces, MutableSequence)

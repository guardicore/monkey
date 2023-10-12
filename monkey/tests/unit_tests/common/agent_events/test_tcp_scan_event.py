from ipaddress import IPv4Address
from uuid import UUID

import pytest

from common.agent_events import TCPScanEvent
from common.types import PortStatus

TARGET_IP_STR = "192.168.1.10"
AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")

TCP_SCAN_EVENT = TCPScanEvent(
    source=AGENT_ID,
    timestamp=1664371327.4067292,
    target=IPv4Address(TARGET_IP_STR),
    ports={
        22: PortStatus.OPEN,
        80: PortStatus.CLOSED,
        443: PortStatus.OPEN,
        8080: PortStatus.CLOSED,
    },
)

TCP_OBJECT_DICT = {
    "source": AGENT_ID,
    "timestamp": 1664371327.4067292,
    "target": IPv4Address(TARGET_IP_STR),
    "ports": {
        22: PortStatus.OPEN,
        80: PortStatus.CLOSED,
        443: PortStatus.OPEN,
        8080: PortStatus.CLOSED,
    },
}

TCP_SIMPLE_DICT = {
    "source": str(AGENT_ID),
    "timestamp": 1664371327.4067292,
    "target": TARGET_IP_STR,
    "ports": {
        22: "open",
        80: "closed",
        443: "open",
        8080: "closed",
    },
}


@pytest.mark.parametrize("tcp_event_dict", [TCP_OBJECT_DICT, TCP_SIMPLE_DICT])
def test_constructor(tcp_event_dict):
    assert TCPScanEvent(**tcp_event_dict) == TCP_SCAN_EVENT


def test_to_dict():
    TCP_SCAN_EVENT.model_dump(mode="json") == TCP_SIMPLE_DICT


@pytest.mark.parametrize(
    "key, value",
    [
        ("ports", "not-a-dict"),
    ],
)
def test_construct_invalid_field__type_error(key, value):
    invalid_type_dict = TCP_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(TypeError):
        TCPScanEvent(**invalid_type_dict)


@pytest.mark.parametrize(
    "key, value",
    [
        ("target", None),
        ("target", "not-an-ip"),
        ("ports", {99999: "closed"}),
        ("ports", {"not-a-number": "open"}),
        ("ports", {22: "bogus"}),
    ],
)
def test_construct_invalid_field__value_error(key, value):
    invalid_type_dict = TCP_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(ValueError):
        TCPScanEvent(**invalid_type_dict)


def test_construct__extra_fields_forbidden():
    extra_field_dict = TCP_SIMPLE_DICT.copy()
    extra_field_dict["extra_field"] = 99  # red balloons

    with pytest.raises(ValueError):
        TCPScanEvent(**extra_field_dict)

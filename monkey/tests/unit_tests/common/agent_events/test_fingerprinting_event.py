from ipaddress import IPv4Address

from monkeytypes import (
    DiscoveredService,
    NetworkPort,
    NetworkProtocol,
    NetworkService,
    OperatingSystem,
)
from tests.unit_tests.monkey_island.cc.models.test_agent import AGENT_ID

from common.agent_events import FingerprintingEvent
from common.types import AgentID

OS_VERSION = "Jammy 22.04"

DISCOVERED_SERVICES = (
    DiscoveredService(
        protocol=NetworkProtocol.TCP, port=NetworkPort(22), service=NetworkService.SSH
    ),
    DiscoveredService(
        protocol=NetworkProtocol.TCP, port=NetworkPort(80), service=NetworkService.HTTP
    ),
    DiscoveredService(
        protocol=NetworkProtocol.TCP, port=NetworkPort(443), service=NetworkService.HTTPS
    ),
    DiscoveredService(
        protocol=NetworkProtocol.UDP, port=NetworkPort(800), service=NetworkService.UNKNOWN
    ),
)

FINGERPRINTING_EVENT = FingerprintingEvent(
    source=AGENT_ID,
    target=IPv4Address("1.1.1.1"),
    timestamp=1664371327.4067292,
    os=OperatingSystem.LINUX,
    os_version=OS_VERSION,
    discovered_services=DISCOVERED_SERVICES,
)

FINGERPRINTING_OBJECT_DICT = {
    "source": AgentID("012e7238-7b81-4108-8c7f-0787bc3f3c10"),
    "target": IPv4Address("1.1.1.1"),
    "timestamp": 1664371327.4067292,
    "tags": frozenset(),
    "os": OperatingSystem.LINUX,
    "os_version": OS_VERSION,
    "discovered_services": DISCOVERED_SERVICES,
}

FINGERPRINTING_SIMPLE_DICT = {
    "source": "012e7238-7b81-4108-8c7f-0787bc3f3c10",
    "target": "1.1.1.1",
    "timestamp": 1664371327.4067292,
    "tags": [],
    "os": "linux",
    "os_version": OS_VERSION,
    "discovered_services": [ds.to_json_dict() for ds in DISCOVERED_SERVICES],
}


def test_constructor():
    assert FingerprintingEvent(**FINGERPRINTING_OBJECT_DICT) == FINGERPRINTING_EVENT


def test_from_dict():
    assert FingerprintingEvent(**FINGERPRINTING_SIMPLE_DICT) == FINGERPRINTING_EVENT


def test_to_dict():
    fingerprinting_event = FingerprintingEvent(**FINGERPRINTING_OBJECT_DICT)

    assert fingerprinting_event.to_json_dict() == FINGERPRINTING_SIMPLE_DICT


def test_deserialization_dict():
    original = FINGERPRINTING_EVENT

    serialized_event = original.to_dict()
    deserialized_event = FingerprintingEvent(**serialized_event)

    assert deserialized_event == original

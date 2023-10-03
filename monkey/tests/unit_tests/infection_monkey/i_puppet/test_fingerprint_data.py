from typing import Any, Dict

import pytest
from monkeytypes import OperatingSystem

from common.types import DiscoveredService, NetworkProtocol, NetworkService
from infection_monkey.i_puppet import FingerprintData

LINUX_VERSION = "xenial"

DISCOVERED_SERVICE_DICT_1 = {"protocol": "tcp", "port": 80, "service": "http"}

DISCOVERED_SERVICE_OBJECT_1 = DiscoveredService(
    protocol=NetworkProtocol.TCP, port=80, service=NetworkService.HTTP
)

DISCOVERED_SERVICE_DICT_2 = {"protocol": "tcp", "port": 443, "service": "https"}

DISCOVERED_SERVICE_OBJECT_2 = DiscoveredService(
    protocol=NetworkProtocol.TCP, port=443, service=NetworkService.HTTPS
)


DISCOVERED_SERVICE_DICT_3 = {"protocol": "tcp", "port": 22, "service": "ssh"}

DISCOVERED_SERVICE_OBJECT_3 = DiscoveredService(
    protocol=NetworkProtocol.TCP, port=22, service=NetworkService.SSH
)


FINGERPRINT_DATA_DICT_IN: Dict[str, Any] = {
    "os_type": "linux",
    "os_version": LINUX_VERSION,
    "services": [DISCOVERED_SERVICE_DICT_3, DISCOVERED_SERVICE_DICT_2],
}

FINGERPRINT_DATA_OBJECT = FingerprintData(
    os_type=OperatingSystem.LINUX,
    os_version=LINUX_VERSION,
    services=[DISCOVERED_SERVICE_OBJECT_3, DISCOVERED_SERVICE_OBJECT_2],
)


def test_fingerprint_data__serialization():
    assert FINGERPRINT_DATA_OBJECT.dict(simplify=True) == FINGERPRINT_DATA_DICT_IN


def test_fingerprint_data__deserialization():
    assert FingerprintData(**FINGERPRINT_DATA_DICT_IN) == FINGERPRINT_DATA_OBJECT


@pytest.mark.parametrize(
    "discovered_service_object, discovered_service_dict",
    [
        (DISCOVERED_SERVICE_OBJECT_1, DISCOVERED_SERVICE_DICT_1),
        (DISCOVERED_SERVICE_OBJECT_2, DISCOVERED_SERVICE_DICT_2),
        (DISCOVERED_SERVICE_OBJECT_3, DISCOVERED_SERVICE_DICT_3),
    ],
)
def test_discovered_service__serialization(discovered_service_object, discovered_service_dict):
    assert discovered_service_object.dict(simplify=True) == discovered_service_dict


@pytest.mark.parametrize(
    "discovered_service_object, discovered_service_dict",
    [
        (DISCOVERED_SERVICE_OBJECT_1, DISCOVERED_SERVICE_DICT_1),
        (DISCOVERED_SERVICE_OBJECT_2, DISCOVERED_SERVICE_DICT_2),
        (DISCOVERED_SERVICE_OBJECT_3, DISCOVERED_SERVICE_DICT_3),
    ],
)
def test_discovered_service__deserialization(discovered_service_object, discovered_service_dict):
    assert DiscoveredService(**discovered_service_dict) == discovered_service_object


@pytest.mark.parametrize("port", ["", 70000, None, -12342])
def test_discovered_service__invalid_port(port):
    with pytest.raises(ValueError):
        DiscoveredService(portocol=NetworkProtocol.TCP, port=port, service=NetworkService.SSH)

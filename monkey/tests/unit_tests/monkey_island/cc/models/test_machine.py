import uuid
from ipaddress import IPv4Interface
from types import MappingProxyType
from typing import MutableSequence

import pytest
from monkeytypes import IllegalMutationError, OperatingSystem

from common.types import NetworkService, SocketAddress
from monkey_island.cc.models import Machine

SOCKET_ADDR_1 = "192.168.1.10:5000"
SOCKET_ADDR_2 = "192.168.1.10:8080"

MACHINE_OBJECT_DICT = MappingProxyType(
    {
        "id": 1,
        "hardware_id": uuid.getnode(),
        "island": True,
        "network_interfaces": [IPv4Interface("10.0.0.1/24"), IPv4Interface("192.168.5.32/16")],
        "operating_system": OperatingSystem.WINDOWS,
        "operating_system_version": "eXtra Problems",
        "hostname": "my.host",
        "network_services": {
            SocketAddress.from_string(SOCKET_ADDR_1): NetworkService.UNKNOWN,
            SocketAddress.from_string(SOCKET_ADDR_2): NetworkService.UNKNOWN,
        },
    }
)

MACHINE_SIMPLE_DICT = MappingProxyType(
    {
        "id": 1,
        "hardware_id": uuid.getnode(),
        "island": True,
        "network_interfaces": ["10.0.0.1/24", "192.168.5.32/16"],
        "operating_system": OperatingSystem.WINDOWS.value,
        "operating_system_version": "eXtra Problems",
        "hostname": "my.host",
        "network_services": {
            SOCKET_ADDR_1: NetworkService.UNKNOWN.value,
            SOCKET_ADDR_2: NetworkService.UNKNOWN.value,
        },
    }
)


def test_constructor():
    # Raises exception_on_failure
    Machine(**MACHINE_OBJECT_DICT)


def test_from_dict():
    # Raises exception_on_failure
    Machine(**MACHINE_SIMPLE_DICT)


def test_to_dict():
    m = Machine(**MACHINE_OBJECT_DICT)

    assert m.to_json_dict() == dict(MACHINE_SIMPLE_DICT)


@pytest.mark.parametrize(
    "key, value",
    [
        ("network_interfaces", "not-a-list"),
        ("operating_system_version", {}),
        ("hostname", []),
        ("network_services", 42),
        ("network_services", [SOCKET_ADDR_1]),
        ("network_services", None),
    ],
)
def test_construct_invalid_field__type_error(key, value):
    invalid_type_dict = MACHINE_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(TypeError):
        Machine(**invalid_type_dict)


@pytest.mark.parametrize(
    "key, value",
    [
        ("id", -1),
        ("id", "not-an-int"),
        ("island", "not-a-bool"),
        ("hardware_id", 0),
        ("hardware_id", "not-an-int"),
        ("operating_system", 2.1),
        ("operating_system", "bsd"),
        ("network_interfaces", [1, "stuff", 3]),
        ("network_interfaces", ["10.0.0.1/16", 2, []]),
        ("network_services", {"192.168.": NetworkService.UNKNOWN.value}),
        ("network_services", {SOCKET_ADDR_1: "Hello"}),
        ("network_services", {SocketAddress.from_string(SOCKET_ADDR_1): "Hello"}),
    ],
)
def test_construct_invalid_field__value_error(key, value):
    invalid_type_dict = MACHINE_SIMPLE_DICT.copy()
    invalid_type_dict[key] = value

    with pytest.raises(ValueError):
        Machine(**invalid_type_dict)


@pytest.mark.parametrize("field", ["hardware_id", "operating_system"])
def test_optional_fields(field):
    none_field_dict = MACHINE_SIMPLE_DICT.copy()
    none_field_dict[field] = None

    # Raises exception_on_failure
    Machine(**none_field_dict)


def test_construct__extra_fields_forbidden():
    extra_field_dict = MACHINE_SIMPLE_DICT.copy()
    extra_field_dict["extra_field"] = 99  # red balloons

    with pytest.raises(ValueError):
        Machine(**extra_field_dict)


def test_id_immutable():
    m = Machine(**MACHINE_OBJECT_DICT)
    with pytest.raises(IllegalMutationError):
        m.id = 2


@pytest.mark.parametrize("hardware_id", [None, 1, 100])
def test_hardware_id_set_valid_value(hardware_id):
    m = Machine(**MACHINE_OBJECT_DICT)

    # Raises exception_on_failure
    m.hardware_id = hardware_id


def test_hardware_id_validate_on_set():
    m = Machine(**MACHINE_OBJECT_DICT)
    with pytest.raises(ValueError):
        m.hardware_id = -50


def test_hardware_id_default():
    missing_hardware_id_dict = MACHINE_OBJECT_DICT.copy()
    del missing_hardware_id_dict["hardware_id"]

    m = Machine(**missing_hardware_id_dict)

    assert m.hardware_id is None


def test_island_immutable():
    m = Machine(**MACHINE_OBJECT_DICT)
    with pytest.raises(IllegalMutationError):
        m.island = True


def test_island_default():
    missing_island_dict = MACHINE_OBJECT_DICT.copy()
    del missing_island_dict["island"]

    m = Machine(**missing_island_dict)

    assert m.island is False


def test_network_interfaces_set_valid_value():
    m = Machine(**MACHINE_OBJECT_DICT)

    # Raises exception_on_failure
    m.network_interfaces = [IPv4Interface("172.1.2.3/24")]


def test_network_interfaces_set_invalid_value():
    m = Machine(**MACHINE_OBJECT_DICT)

    with pytest.raises(ValueError):
        m.network_interfaces = [IPv4Interface("172.1.2.3/24"), None]


def test_network_interfaces_sequence_is_immutable():
    m = Machine(**MACHINE_OBJECT_DICT)

    assert not isinstance(m.network_interfaces, MutableSequence)


def test_network_interfaces_default():
    missing_network_interfaces_dict = MACHINE_OBJECT_DICT.copy()
    del missing_network_interfaces_dict["network_interfaces"]

    m = Machine(**missing_network_interfaces_dict)

    assert len(m.network_interfaces) == 0


def test_operating_system_set_valid_value():
    m = Machine(**MACHINE_OBJECT_DICT)

    # Raises exception_on_failure
    m.operating_system = OperatingSystem.LINUX


def test_operating_system_set_invalid_value():
    m = Machine(**MACHINE_OBJECT_DICT)

    with pytest.raises(ValueError):
        m.operating_system = "MacOS"


def test_operating_system_default_value():
    missing_operating_system_dict = MACHINE_OBJECT_DICT.copy()
    del missing_operating_system_dict["operating_system"]

    m = Machine(**missing_operating_system_dict)

    assert m.operating_system is None


def test_set_operating_system_version():
    m = Machine(**MACHINE_OBJECT_DICT)

    # Raises exception_on_failure
    m.operating_system_version = "1234"


def test_operating_system_version_default_value():
    missing_operating_system_version_dict = MACHINE_OBJECT_DICT.copy()
    del missing_operating_system_version_dict["operating_system_version"]

    m = Machine(**missing_operating_system_version_dict)

    assert m.operating_system_version == ""


def test_set_hostname():
    m = Machine(**MACHINE_OBJECT_DICT)

    # Raises exception_on_failure
    m.operating_system_version = "wopr"


def test_hostname_default_value():
    missing_hostname_dict = MACHINE_OBJECT_DICT.copy()
    del missing_hostname_dict["hostname"]

    m = Machine(**missing_hostname_dict)

    assert m.hostname == ""


def test_set_network_services_validates():
    m = Machine(**MACHINE_OBJECT_DICT)

    with pytest.raises(ValueError):
        m.network_services = {"not-an-ip": NetworkService.UNKNOWN.value}


def test_set_network_services_default_value():
    missing_network_services = MACHINE_OBJECT_DICT.copy()
    del missing_network_services["network_services"]

    m = Machine(**missing_network_services)

    assert m.network_services == {}

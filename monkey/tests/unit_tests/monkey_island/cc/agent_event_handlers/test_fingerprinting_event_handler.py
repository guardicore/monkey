from ipaddress import IPv4Address, IPv4Interface
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from monkeytypes import OperatingSystem, SocketAddress

from common.agent_events import FingerprintingEvent
from common.types import DiscoveredService, NetworkPort, NetworkProtocol, NetworkService
from monkey_island.cc.agent_event_handlers import FingerprintingEventHandler
from monkey_island.cc.models import Machine
from monkey_island.cc.repositories import IMachineRepository, NetworkModelUpdateFacade

AGENT_ID = UUID("1d8ce743-a0f4-45c5-96af-91106529d3e2")
TARGET_MACHINE_IP = IPv4Address("10.10.10.1")
TARGET_MACHINE_ID = 33
SEED_ID = 99


DISCOVERED_SERVICES = (
    DiscoveredService(
        protocol=NetworkProtocol.TCP, port=NetworkPort(5000), service=NetworkService.HTTPS
    ),
    DiscoveredService(
        protocol=NetworkProtocol.UDP, port=NetworkPort(5001), service=NetworkService.MSSQL
    ),
)

NETWORK_SERVICES = {
    SocketAddress(ip=TARGET_MACHINE_IP, port=NetworkPort(5000)): NetworkService.HTTPS,
    SocketAddress(ip=TARGET_MACHINE_IP, port=NetworkPort(5001)): NetworkService.MSSQL,
}


FINGERPRINTING_EVENT_NO_OS_INFO_NO_SERVICES = FingerprintingEvent(
    source=AGENT_ID,
    target=TARGET_MACHINE_IP,
)

FINGERPRINTING_EVENT_NO_SERVICES = FingerprintingEvent(
    source=AGENT_ID,
    target=TARGET_MACHINE_IP,
    os=OperatingSystem.LINUX,
    os_version="Debian",
)

FINGERPRINTING_EVENT_NO_OS_INFO = FingerprintingEvent(
    source=AGENT_ID, target=TARGET_MACHINE_IP, discovered_services=DISCOVERED_SERVICES
)

FINGERPRINTING_EVENT = FingerprintingEvent(
    source=AGENT_ID,
    target=TARGET_MACHINE_IP,
    os=OperatingSystem.WINDOWS,
    os_version="XP",
    discovered_services=DISCOVERED_SERVICES,
)


@pytest.fixture
def target_machine() -> Machine:
    return Machine(
        id=TARGET_MACHINE_ID,
        hardware_id=9,
        network_interfaces=[IPv4Interface(f"{TARGET_MACHINE_IP}/24")],
    )


@pytest.fixture
def machine_repository() -> IMachineRepository:
    return MagicMock(spec=IMachineRepository)


@pytest.fixture
def network_model_update_facade(target_machine) -> NetworkModelUpdateFacade:
    network_model_update_facade = MagicMock(ispec=NetworkModelUpdateFacade)
    network_model_update_facade.get_or_create_target_machine = lambda target: target_machine
    return network_model_update_facade


@pytest.fixture
def fingerprinting_event_handler(network_model_update_facade, machine_repository):
    return FingerprintingEventHandler(network_model_update_facade, machine_repository)


def test_fingerprinting_event_handler(
    fingerprinting_event_handler, machine_repository: IMachineRepository
):
    fingerprinting_event_handler.handle_fingerprinting_event(FINGERPRINTING_EVENT)

    assert machine_repository.upsert_machine.call_count == 2
    assert machine_repository.upsert_network_services.call_count == 1
    machine_repository.upsert_network_services.assert_called_with(
        TARGET_MACHINE_ID, NETWORK_SERVICES
    )


def test_fingerprinting_event_handler__no_services(
    fingerprinting_event_handler, machine_repository: IMachineRepository
):
    fingerprinting_event_handler.handle_fingerprinting_event(FINGERPRINTING_EVENT_NO_SERVICES)

    assert machine_repository.upsert_machine.call_count == 2
    assert machine_repository.upsert_network_services.call_count == 0


def test_fingerprinting_event_handler__no_os_info(
    fingerprinting_event_handler, machine_repository: IMachineRepository
):
    fingerprinting_event_handler.handle_fingerprinting_event(FINGERPRINTING_EVENT_NO_OS_INFO)

    assert machine_repository.upsert_machine.call_count == 0
    assert machine_repository.upsert_network_services.call_count == 1
    machine_repository.upsert_network_services.assert_called_with(
        TARGET_MACHINE_ID, NETWORK_SERVICES
    )


def test_fingerprinting_event_handler__no_os_info_no_services(
    fingerprinting_event_handler, machine_repository: IMachineRepository
):
    fingerprinting_event_handler.handle_fingerprinting_event(
        FINGERPRINTING_EVENT_NO_OS_INFO_NO_SERVICES
    )

    assert machine_repository.upsert_machine.call_count == 0
    assert machine_repository.upsert_network_services.call_count == 0

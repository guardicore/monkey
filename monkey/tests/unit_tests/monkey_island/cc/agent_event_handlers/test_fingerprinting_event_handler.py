from ipaddress import IPv4Address, IPv4Interface
from itertools import count
from typing import Callable, Dict, Sequence
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from common import OperatingSystem
from common.agent_events import FingerprintingEvent
from common.types import (
    DiscoveredService,
    MachineID,
    NetworkPort,
    NetworkProtocol,
    NetworkService,
    SocketAddress,
)
from monkey_island.cc.agent_event_handlers import FingerprintingEventHandler
from monkey_island.cc.models import Machine
from monkey_island.cc.repositories import (
    IAgentRepository,
    IMachineRepository,
    NetworkModelUpdateFacade,
    UnknownRecordError,
)

AGENT_ID = UUID("1d8ce743-a0f4-45c5-96af-91106529d3e2")
TARGET_MACHINE_IP = "10.10.10.1"
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
    target=IPv4Address(TARGET_MACHINE_IP),
)

FINGERPRINTING_EVENT_NO_SERVICES = FingerprintingEvent(
    source=AGENT_ID,
    target=IPv4Address(TARGET_MACHINE_IP),
    os=OperatingSystem.LINUX,
    os_version="Debian",
)

FINGERPRINTING_EVENT_NO_OS_INFO = FingerprintingEvent(
    source=AGENT_ID, target=IPv4Address(TARGET_MACHINE_IP), discovered_services=DISCOVERED_SERVICES
)

FINGERPRINTING_EVENT = FingerprintingEvent(
    source=AGENT_ID,
    target=IPv4Address(TARGET_MACHINE_IP),
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
def agent_repository() -> IAgentRepository:
    return MagicMock(spec=IAgentRepository)


@pytest.fixture
def machine_repository(
    machine_from_id: Callable[[MachineID], Machine],
    machines_from_ip: Callable[[IPv4Address], Sequence[Machine]],
) -> IMachineRepository:
    machine_repository = MagicMock(spec=IMachineRepository)
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(side_effect=machines_from_ip)
    machine_repository.get_new_id = MagicMock(side_effect=count(SEED_ID))
    return machine_repository


@pytest.fixture
def network_model_update_facade(machine_repository):
    return NetworkModelUpdateFacade(MagicMock(), machine_repository, MagicMock())


@pytest.fixture
def fingerprinting_event_handler(network_model_update_facade, machine_repository):
    return FingerprintingEventHandler(network_model_update_facade, machine_repository)


@pytest.fixture
def machines_by_id(target_machine: Machine) -> Dict[MachineID, Machine]:
    return {target_machine.id: target_machine}


@pytest.fixture
def machines_by_ip(target_machine: Machine) -> Dict[IPv4Address, Sequence[Machine]]:
    return {IPv4Address(TARGET_MACHINE_IP): [target_machine]}


@pytest.fixture
def machine_from_id(machines_by_id) -> Callable[[MachineID], Machine]:
    def inner(id: int) -> Machine:
        return machines_by_id[id]

    return inner


@pytest.fixture
def machines_from_ip(machines_by_ip) -> Callable[[IPv4Address], Sequence[Machine]]:
    def inner(ip: IPv4Address) -> Sequence[Machine]:
        return machines_by_ip[ip]

    return inner


def test_fingerprinting_event_handler__target_machine_does_not_exist(
    fingerprinting_event_handler, machine_repository: IMachineRepository
):
    event = FINGERPRINTING_EVENT_NO_OS_INFO
    machine_repository.get_machines_by_ip = MagicMock(side_effect=UnknownRecordError)

    fingerprinting_event_handler.handle_fingerprinting_event(event)

    expected_machine = Machine(id=SEED_ID, network_interfaces=[IPv4Interface(event.target)])

    machine_repository.upsert_machine.assert_any_call(expected_machine)


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

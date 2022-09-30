from ipaddress import IPv4Address, IPv4Interface
from itertools import count
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from common import OperatingSystem
from common.agent_events import PingScanEvent
from common.types import SocketAddress
from monkey_island.cc.agent_event_handlers import handle_ping_scan_event
from monkey_island.cc.models import Agent, CommunicationType, Machine
from monkey_island.cc.repository import (
    IAgentRepository,
    IMachineRepository,
    INodeRepository,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)

SEED_ID = 99
AGENT_ID = UUID("1d8ce743-a0f4-45c5-96af-91106529d3e2")
MACHINE_ID = 11
CC_SERVER = SocketAddress(ip="10.10.10.100", port="5000")
AGENT = Agent(id=AGENT_ID, machine_id=MACHINE_ID, start_time=0, parent_id=None, cc_server=CC_SERVER)
PINGER_MACHINE = Machine(
    id=MACHINE_ID,
    hardware_id=5,
    network_interfaces=[IPv4Interface("10.10.10.99/24")],
)
TARGET_MACHINE = Machine(
    id=33,
    hardware_id=9,
    network_interfaces=[IPv4Interface("10.10.10.1/24")],
)
EVENT = PingScanEvent(
    source=AGENT_ID,
    target=IPv4Address("10.10.10.1"),
    response_received=True,
    os=OperatingSystem.LINUX,
)

EVENT_NO_RESPONSE = PingScanEvent(
    source=AGENT_ID,
    target=IPv4Address("10.10.10.1"),
    response_received=False,
    os=OperatingSystem.LINUX,
)


@pytest.fixture
def agent_repository() -> IAgentRepository:
    agent_repository = MagicMock(spec=IAgentRepository)
    agent_repository.upsert_agent = MagicMock()
    agent_repository.get_agent_by_id = MagicMock(return_value=AGENT)
    return agent_repository


@pytest.fixture
def machine_repository() -> IMachineRepository:
    machine_repository = MagicMock(spec=IMachineRepository)
    machine_repository.get_new_id = MagicMock(side_effect=count(SEED_ID))
    machine_repository.upsert_machine = MagicMock()
    return machine_repository


@pytest.fixture
def node_repository() -> INodeRepository:
    node_repository = MagicMock(spec=INodeRepository)
    node_repository.upsert_communication = MagicMock()
    return node_repository


@pytest.fixture
def handler(agent_repository, machine_repository, node_repository) -> handle_ping_scan_event:
    return handle_ping_scan_event(agent_repository, machine_repository, node_repository)


machines = {MACHINE_ID: PINGER_MACHINE, TARGET_MACHINE.id: TARGET_MACHINE}
machines_by_id = {MACHINE_ID: PINGER_MACHINE, TARGET_MACHINE.id: TARGET_MACHINE}
machines_by_ip = {
    IPv4Address("10.10.10.99"): [PINGER_MACHINE],
    IPv4Address("10.10.10.1"): [TARGET_MACHINE],
}


def machine_from_id(id: int):
    return machines_by_id[id]


def machines_from_ip(ip: IPv4Address):
    return machines_by_ip[ip]


class error_machine_by_id:
    """Raise an error if the machine with the called ID matches the stored ID"""

    def __init__(self, id: int, error):
        self.id = id
        self.error = error

    def __call__(self, id: int):
        if id == self.id:
            raise self.error
        else:
            return machine_from_id(id)


class error_machine_by_ip:
    """Raise an error if the machine with the called IP matches the stored ID"""

    def __init__(self, id: int, error):
        self.id = id
        self.error = error

    def __call__(self, ip: IPv4Address):
        print(f"IP is: {ip}")
        machines = machines_from_ip(ip)
        if machines[0].id == self.id:
            print(f"Raise error: {self.error}")
            raise self.error
        else:
            print(f"Return machine: {machines}")
            return machines


def test_handle_ping_scan_event__target_machine_not_exists(
    handler: handle_ping_scan_event,
    machine_repository: IMachineRepository,
):
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(side_effect=UnknownRecordError)

    handler(EVENT)

    expected_machine = Machine(id=SEED_ID, network_interfaces=[IPv4Interface(EVENT.target)])
    expected_machine.operating_system = EVENT.os
    machine_repository.upsert_machine.assert_called_with(expected_machine)


def test_handle_ping_scan_event__target_machine_already_exists(
    handler: handle_ping_scan_event,
    machine_repository: IMachineRepository,
):
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(side_effect=machines_from_ip)

    handler(EVENT)

    expected_machine = TARGET_MACHINE.copy()
    expected_machine.operating_system = OperatingSystem.LINUX
    machine_repository.upsert_machine.assert_called_with(expected_machine)


def test_handle_ping_scan_event__upserts_node(
    handler: handle_ping_scan_event,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
):
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(return_value=[TARGET_MACHINE])

    handler(EVENT)

    node_repository.upsert_communication.assert_called_with(
        PINGER_MACHINE.id, TARGET_MACHINE.id, CommunicationType.SCANNED
    )


def test_handle_ping_scan_event__node_not_upserted_if_no_matching_agent(
    handler: handle_ping_scan_event,
    agent_repository: IAgentRepository,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
):
    agent_repository.get_agent_by_id = MagicMock(side_effect=UnknownRecordError)
    machine_repository.get_machine_by_id = MagicMock(return_value=TARGET_MACHINE)

    handler(EVENT)

    assert not node_repository.upsert_communication.called


def test_handle_ping_scan_event__node_not_upserted_if_no_matching_machine(
    handler: handle_ping_scan_event,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
):
    machine_repository.get_machine_by_id = MagicMock(side_effect=UnknownRecordError)

    handler(EVENT)

    assert not node_repository.upsert_communication.called


@pytest.mark.parametrize("id", [PINGER_MACHINE.id, TARGET_MACHINE.id])
def test_handle_scan_data__node_not_upserted_if_machine_retrievalerror(
    handler: handle_ping_scan_event,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
    id,
):
    machine_repository.get_machine_by_id = MagicMock(
        side_effect=error_machine_by_id(id, RetrievalError)
    )
    machine_repository.get_machines_by_ip = MagicMock(
        side_effect=error_machine_by_ip(id, RetrievalError)
    )

    handler(EVENT)

    assert not node_repository.upsert_communication.called


def test_handle_scan_data__machine_not_upserted_if_os_is_none(
    handler: handle_ping_scan_event, machine_repository: IMachineRepository
):
    event = PingScanEvent(source=EVENT.source, target=EVENT.target, response_received=True, os=None)
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(side_effect=machines_from_ip)

    handler(event)

    assert not machine_repository.upsert_machine.called


def test_handle_scan_data__machine_not_upserted_if_existing_machine_has_os(
    handler: handle_ping_scan_event, machine_repository: IMachineRepository
):
    machine_with_os = TARGET_MACHINE
    machine_with_os.operating_system = OperatingSystem.WINDOWS
    machine_repository.get_machine_by_ip = MagicMock(return_value=machine_with_os)

    handler(EVENT)

    assert not machine_repository.upsert_machine.called


def test_handle_scan_data__node_not_upserted_if_machine_storageerror(
    handler: handle_ping_scan_event,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
):
    target_machine = TARGET_MACHINE
    target_machine.operating_system = None
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(return_value=target_machine)
    machine_repository.upsert_machine = MagicMock(side_effect=StorageError)

    handler(EVENT)

    assert not node_repository.upsert_communication.called


def test_handle_scan_data__failed_ping(
    handler: handle_ping_scan_event,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
):
    machine_repository.upsert_machine = MagicMock(side_effect=StorageError)
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(side_effect=machines_from_ip)

    handler(EVENT_NO_RESPONSE)

    assert not node_repository.upsert_communication.called
    assert not machine_repository.upsert_machine.called

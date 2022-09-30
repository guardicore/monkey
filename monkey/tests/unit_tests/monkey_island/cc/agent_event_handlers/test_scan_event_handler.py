from ipaddress import IPv4Address, IPv4Interface
from itertools import count
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from common import OperatingSystem
from common.agent_events import PingScanEvent, TCPScanEvent
from common.types import PortStatus, SocketAddress
from monkey_island.cc.agent_event_handlers import ScanEventHandler
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
SOURCE_MACHINE = Machine(
    id=MACHINE_ID,
    hardware_id=5,
    network_interfaces=[IPv4Interface("10.10.10.99/24")],
)
TARGET_MACHINE = Machine(
    id=33,
    hardware_id=9,
    network_interfaces=[IPv4Interface("10.10.10.1/24")],
)

PING_SCAN_EVENT = PingScanEvent(
    source=AGENT_ID,
    target=IPv4Address("10.10.10.1"),
    response_received=True,
    os=OperatingSystem.LINUX,
)

PING_SCAN_EVENT_NO_RESPONSE = PingScanEvent(
    source=AGENT_ID,
    target=IPv4Address("10.10.10.1"),
    response_received=False,
    os=OperatingSystem.LINUX,
)

PING_SCAN_EVENT_NO_OS = PingScanEvent(
    source=AGENT_ID,
    target=IPv4Address("10.10.10.1"),
    response_received=True,
    os=None,
)


TCP_SCAN_EVENT = TCPScanEvent(
    source=AGENT_ID,
    target=IPv4Address("10.10.10.1"),
    ports={22: PortStatus.OPEN, 8080: PortStatus.CLOSED},
)

TCP_SCAN_EVENT_CLOSED = TCPScanEvent(
    source=AGENT_ID,
    target=IPv4Address("10.10.10.1"),
    ports={145: PortStatus.CLOSED, 8080: PortStatus.CLOSED},
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
def scan_event_handler(agent_repository, machine_repository, node_repository):
    return ScanEventHandler(agent_repository, machine_repository, node_repository)


machines = {MACHINE_ID: SOURCE_MACHINE, TARGET_MACHINE.id: TARGET_MACHINE}
machines_by_id = {MACHINE_ID: SOURCE_MACHINE, TARGET_MACHINE.id: TARGET_MACHINE}
machines_by_ip = {
    IPv4Address("10.10.10.99"): [SOURCE_MACHINE],
    IPv4Address("10.10.10.1"): [TARGET_MACHINE],
}


@pytest.fixture(params=[SOURCE_MACHINE.id, TARGET_MACHINE.id])
def machine_id(request):
    return request.param


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


HANDLE_PING_SCAN_METHOD = "handle_ping_scan_event"
HANDLE_TCP_SCAN_METHOD = "handle_tcp_scan_event"


@pytest.fixture
def handler(scan_event_handler, request):
    return getattr(scan_event_handler, request.param)


@pytest.mark.parametrize(
    "event,handler",
    [(PING_SCAN_EVENT, HANDLE_PING_SCAN_METHOD), (TCP_SCAN_EVENT, HANDLE_TCP_SCAN_METHOD)],
    indirect=["handler"],
)
def test_target_machine_not_exists(event, handler, machine_repository: IMachineRepository, request):
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(side_effect=UnknownRecordError)

    handler(event)

    expected_machine = Machine(id=SEED_ID, network_interfaces=[IPv4Interface(event.target)])
    if event == PING_SCAN_EVENT:
        expected_machine.operating_system = event.os
    machine_repository.upsert_machine.assert_called_with(expected_machine)


@pytest.mark.parametrize(
    "event,handler",
    [(PING_SCAN_EVENT, HANDLE_PING_SCAN_METHOD), (TCP_SCAN_EVENT, HANDLE_TCP_SCAN_METHOD)],
    indirect=["handler"],
)
def test_upserts_node(
    event,
    handler,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
    request,
):
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(return_value=[TARGET_MACHINE])

    handler(event)

    node_repository.upsert_communication.assert_called_with(
        SOURCE_MACHINE.id, TARGET_MACHINE.id, CommunicationType.SCANNED
    )


@pytest.mark.parametrize(
    "event,handler",
    [(PING_SCAN_EVENT, HANDLE_PING_SCAN_METHOD), (TCP_SCAN_EVENT, HANDLE_TCP_SCAN_METHOD)],
    indirect=["handler"],
)
def test_node_not_upserted_if_no_matching_agent(
    event,
    handler,
    agent_repository: IAgentRepository,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
    request,
):
    agent_repository.get_agent_by_id = MagicMock(side_effect=UnknownRecordError)
    machine_repository.get_machine_by_id = MagicMock(return_value=TARGET_MACHINE)

    handler(event)

    assert not node_repository.upsert_communication.called


@pytest.mark.parametrize(
    "event,handler",
    [(PING_SCAN_EVENT, HANDLE_PING_SCAN_METHOD), (TCP_SCAN_EVENT, HANDLE_TCP_SCAN_METHOD)],
    indirect=["handler"],
)
def test_node_not_upserted_if_machine_retrievalerror(
    event,
    handler,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
    request,
    machine_id,
):
    machine_repository.get_machine_by_id = MagicMock(
        side_effect=error_machine_by_id(machine_id, RetrievalError)
    )
    machine_repository.get_machines_by_ip = MagicMock(
        side_effect=error_machine_by_ip(machine_id, RetrievalError)
    )

    handler(event)

    assert not node_repository.upsert_communication.called


@pytest.mark.parametrize(
    "event,handler",
    [
        (PING_SCAN_EVENT_NO_OS, HANDLE_PING_SCAN_METHOD),
        (TCP_SCAN_EVENT_CLOSED, HANDLE_TCP_SCAN_METHOD),
    ],
    indirect=["handler"],
)
def test_machine_not_upserted(event, handler, machine_repository: IMachineRepository, request):
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(side_effect=machines_from_ip)

    handler(event)

    assert not machine_repository.upsert_machine.called


def test_machine_not_upserted_if_existing_machine_has_os(
    scan_event_handler, machine_repository: IMachineRepository, request
):
    machine_with_os = TARGET_MACHINE
    machine_with_os.operating_system = OperatingSystem.WINDOWS
    machine_repository.get_machines_by_ip = MagicMock(return_value=[machine_with_os])

    scan_event_handler.handle_ping_scan_event(PING_SCAN_EVENT)

    assert not machine_repository.upsert_machine.called


@pytest.mark.parametrize(
    "event,handler",
    [(PING_SCAN_EVENT, HANDLE_PING_SCAN_METHOD), (TCP_SCAN_EVENT, HANDLE_TCP_SCAN_METHOD)],
    indirect=["handler"],
)
def test_node_not_upserted_if_machine_storageerror(
    event,
    handler,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
    request,
):
    if event == PING_SCAN_EVENT:
        target_machine = TARGET_MACHINE
        target_machine.operating_system = None

    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(side_effect=UnknownRecordError)
    if event == PING_SCAN_EVENT:
        machine_repository.get_machines_by_ip = MagicMock(side_effect=machines_from_ip)
    machine_repository.upsert_machine = MagicMock(side_effect=StorageError)

    handler(event)

    assert not node_repository.upsert_communication.called


@pytest.mark.parametrize(
    "event,handler",
    [
        (PING_SCAN_EVENT_NO_RESPONSE, HANDLE_PING_SCAN_METHOD),
        (TCP_SCAN_EVENT_CLOSED, HANDLE_TCP_SCAN_METHOD),
    ],
    indirect=["handler"],
)
def test_failed_scan(
    event,
    handler,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
    request,
):
    machine_repository.upsert_machine = MagicMock(side_effect=StorageError)
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(side_effect=machines_from_ip)

    handler(event)

    assert not node_repository.upsert_communication.called
    assert not machine_repository.upsert_machine.called

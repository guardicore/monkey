from copy import deepcopy
from ipaddress import IPv4Address, IPv4Interface
from itertools import count
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.monkey_island import InMemoryMachineRepository

from common import OperatingSystem
from common.agent_events import PingScanEvent, TCPScanEvent
from common.types import NetworkService, PortStatus, SocketAddress
from monkey_island.cc.agent_event_handlers import ScanEventHandler
from monkey_island.cc.models import Agent, CommunicationType, Machine, Node
from monkey_island.cc.repositories import (
    AgentMachineFacade,
    IAgentRepository,
    IMachineRepository,
    INodeRepository,
    NetworkModelUpdateFacade,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)

SEED_ID = 99
AGENT_ID = UUID("1d8ce743-a0f4-45c5-96af-91106529d3e2")
SOURCE_MACHINE_ID = 11
CC_SERVER = SocketAddress(ip="10.10.10.100", port="5000")
AGENT_SHA256 = "c21dafe326222ba3ba65f5aebb6ea09c50696bf40eebca184caffe54f102746c"
AGENT = Agent(
    id=AGENT_ID,
    machine_id=SOURCE_MACHINE_ID,
    start_time=0,
    parent_id=None,
    cc_server=CC_SERVER,
    sha256=AGENT_SHA256,
)
SOURCE_MACHINE = Machine(
    id=SOURCE_MACHINE_ID,
    hardware_id=5,
    network_interfaces=[IPv4Interface("10.10.10.99/24")],
)

TARGET_MACHINE_ID = 33
TARGET_MACHINE_IP = "10.10.10.1"
TARGET_MACHINE = Machine(
    id=TARGET_MACHINE_ID,
    hardware_id=9,
    network_interfaces=[IPv4Interface(f"{TARGET_MACHINE_IP}/24")],
)

SOURCE_NODE = Node(
    machine_id=SOURCE_MACHINE.id,
    connections=[],
    tcp_connections={
        44: (SocketAddress(ip="1.1.1.1", port=40), SocketAddress(ip="2.2.2.2", port=50))
    },
)

PING_SCAN_EVENT = PingScanEvent(
    source=AGENT_ID,
    target=IPv4Address(TARGET_MACHINE_IP),
    response_received=True,
    os=OperatingSystem.LINUX,
)

PING_SCAN_EVENT_NO_RESPONSE = PingScanEvent(
    source=AGENT_ID,
    target=IPv4Address(TARGET_MACHINE_IP),
    response_received=False,
    os=OperatingSystem.LINUX,
)

PING_SCAN_EVENT_NO_OS = PingScanEvent(
    source=AGENT_ID,
    target=IPv4Address(TARGET_MACHINE_IP),
    response_received=True,
    os=None,
)

TCP_SCAN_EVENT = TCPScanEvent(
    source=AGENT_ID,
    target=IPv4Address(TARGET_MACHINE_IP),
    ports={22: PortStatus.OPEN, 80: PortStatus.OPEN, 8080: PortStatus.CLOSED},
)

EXPECTED_NETWORK_SERVICES = {
    SocketAddress(ip=TARGET_MACHINE_IP, port=22): NetworkService.UNKNOWN,
    SocketAddress(ip=TARGET_MACHINE_IP, port=80): NetworkService.UNKNOWN,
}

TCP_CONNECTIONS = {
    TARGET_MACHINE_ID: (
        SocketAddress(ip=TARGET_MACHINE_IP, port=22),
        SocketAddress(ip=TARGET_MACHINE_IP, port=80),
    )
}

TCP_SCAN_EVENT_CLOSED = TCPScanEvent(
    source=AGENT_ID,
    target=IPv4Address(TARGET_MACHINE_IP),
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
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    machine_repository.get_machines_by_ip = MagicMock(side_effect=machines_from_ip)
    machine_repository.get_new_id = MagicMock(side_effect=count(SEED_ID))
    machine_repository.upsert_machine = MagicMock()
    return machine_repository


@pytest.fixture
def in_memory_machine_repository() -> IMachineRepository:
    return InMemoryMachineRepository(SEED_ID)


@pytest.fixture
def node_repository() -> INodeRepository:
    node_repository = MagicMock(spec=INodeRepository)
    node_repository.get_nodes.return_value = [deepcopy(SOURCE_NODE)]
    node_repository.upsert_communication = MagicMock()
    return node_repository


@pytest.fixture
def agent_machine_facade(agent_repository, machine_repository):
    return AgentMachineFacade(agent_repository, machine_repository)


@pytest.fixture
def network_model_update_facade(agent_machine_facade, machine_repository, node_repository):
    return NetworkModelUpdateFacade(agent_machine_facade, machine_repository, node_repository)


@pytest.fixture
def scan_event_handler(network_model_update_facade, machine_repository, node_repository):
    return ScanEventHandler(network_model_update_facade, machine_repository, node_repository)


MACHINES_BY_ID = {SOURCE_MACHINE_ID: SOURCE_MACHINE, TARGET_MACHINE.id: TARGET_MACHINE}
MACHINES_BY_IP = {
    IPv4Address("10.10.10.99"): [SOURCE_MACHINE],
    IPv4Address(TARGET_MACHINE_IP): [TARGET_MACHINE],
}


@pytest.fixture(params=[SOURCE_MACHINE.id, TARGET_MACHINE.id])
def machine_id(request):
    return request.param


def machine_from_id(id: int):
    return MACHINES_BY_ID[id]


def machines_from_ip(ip: IPv4Address):
    return MACHINES_BY_IP[ip]


HANDLE_PING_SCAN_METHOD = "handle_ping_scan_event"
HANDLE_TCP_SCAN_METHOD = "handle_tcp_scan_event"


@pytest.fixture
def handler(scan_event_handler, request):
    return getattr(scan_event_handler, request.param)


def test_ping_scan_event_target_machine_not_exists(
    agent_machine_facade: AgentMachineFacade,
    agent_repository: IAgentRepository,
    in_memory_machine_repository: IMachineRepository,
    node_repository,
):
    network_model_update_facade = NetworkModelUpdateFacade(
        agent_machine_facade, in_memory_machine_repository, node_repository
    )
    scan_event_handler = ScanEventHandler(
        network_model_update_facade, in_memory_machine_repository, node_repository
    )
    event = PING_SCAN_EVENT

    scan_event_handler.handle_ping_scan_event(event)

    expected_machine = Machine(id=SEED_ID, network_interfaces=[IPv4Interface(event.target)])
    expected_machine.operating_system = event.os

    assert in_memory_machine_repository.get_machine_by_id(SEED_ID) == expected_machine


def test_tcp_scan_event_target_machine_not_exists(
    scan_event_handler, machine_repository: IMachineRepository
):
    event = TCP_SCAN_EVENT
    machine_repository.get_machines_by_ip = MagicMock(side_effect=UnknownRecordError)

    scan_event_handler.handle_tcp_scan_event(event)

    expected_machine = Machine(id=SEED_ID, network_interfaces=[IPv4Interface(event.target)])
    machine_repository.upsert_machine.assert_any_call(expected_machine)


def test_handle_tcp_scan_event__no_open_ports(
    scan_event_handler, machine_repository, node_repository
):
    event = TCP_SCAN_EVENT_CLOSED
    scan_event_handler.handle_tcp_scan_event(event)

    assert not node_repository.upsert_tcp_connections.called


def test_handle_tcp_scan_event__ports_found(
    scan_event_handler, machine_repository, node_repository
):
    event = TCP_SCAN_EVENT
    node_repository.get_node_by_machine_id.return_value = SOURCE_NODE
    scan_event_handler.handle_tcp_scan_event(event)

    call_args = node_repository.upsert_tcp_connections.call_args[0]
    assert call_args[0] == SOURCE_MACHINE_ID
    assert TARGET_MACHINE_ID in call_args[1]
    open_socket_addresses = call_args[1][TARGET_MACHINE_ID]
    assert set(open_socket_addresses) == set(TCP_CONNECTIONS[TARGET_MACHINE_ID])
    assert len(open_socket_addresses) == len(TCP_CONNECTIONS[TARGET_MACHINE_ID])


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
):
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
):
    agent_repository.get_agent_by_id = MagicMock(side_effect=UnknownRecordError)
    machine_repository.get_machine_by_id = MagicMock(return_value=TARGET_MACHINE)

    with pytest.raises(UnknownRecordError):
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
    agent_repository: IAgentRepository,
    node_repository: INodeRepository,
    machine_id,
):
    agent_repository.get_agent_by_id = MagicMock(side_effect=RetrievalError)

    with pytest.raises(RetrievalError):
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
def test_machine_not_upserted(event, handler, machine_repository: IMachineRepository):
    handler(event)

    assert not machine_repository.upsert_machine.called


def test_machine_not_upserted_if_existing_machine_has_os(
    scan_event_handler, machine_repository: IMachineRepository
):
    machine_with_os = TARGET_MACHINE
    machine_with_os.operating_system = OperatingSystem.WINDOWS
    machine_repository.get_machines_by_ip = MagicMock(return_value=[machine_with_os])

    scan_event_handler.handle_ping_scan_event(PING_SCAN_EVENT)

    assert not machine_repository.upsert_machine.called


def test_node_not_upserted_by_ping_scan_event_if_machine_storageerror(
    scan_event_handler,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
):
    target_machine = TARGET_MACHINE
    target_machine.operating_system = None
    machine_repository.get_machines_by_ip = MagicMock(side_effect=machines_from_ip)
    machine_repository.upsert_machine = MagicMock(side_effect=StorageError)

    with pytest.raises(StorageError):
        scan_event_handler.handle_ping_scan_event(PING_SCAN_EVENT)

    assert not node_repository.upsert_communication.called


def test_node_not_upserted_by_tcp_scan_event_if_machine_storageerror(
    scan_event_handler,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
):
    machine_repository.get_machines_by_ip = MagicMock(side_effect=UnknownRecordError)
    machine_repository.upsert_machine = MagicMock(side_effect=StorageError)

    with pytest.raises(StorageError):
        scan_event_handler.handle_tcp_scan_event(TCP_SCAN_EVENT)

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
):
    machine_repository.upsert_machine = MagicMock(side_effect=StorageError)

    handler(event)

    assert not node_repository.upsert_communication.called
    assert not machine_repository.upsert_machine.called


def test_network_services_handling(scan_event_handler, machine_repository):
    scan_event_handler.handle_tcp_scan_event(TCP_SCAN_EVENT)

    machine_repository.upsert_network_services.assert_called_with(
        TARGET_MACHINE_ID, EXPECTED_NETWORK_SERVICES
    )

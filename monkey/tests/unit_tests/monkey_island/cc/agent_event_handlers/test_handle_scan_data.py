from ipaddress import IPv4Address, IPv4Interface
from itertools import count
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from common import OperatingSystem
from common.agent_events import PingScanEvent
from common.types import PingScanData, SocketAddress
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
MACHINE = Machine(
    id=MACHINE_ID,
    hardware_id=5,
    network_interfaces=[IPv4Interface("10.10.10.99/24")],
)
STORED_MACHINE = Machine(
    id=33,
    hardware_id=9,
    network_interfaces=[IPv4Interface("10.10.10.1/24")],
)
EVENT = PingScanEvent(
    source=AGENT_ID,
    target=IPv4Address("10.10.10.1"),
    scan_data=PingScanData(True, OperatingSystem.LINUX),
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


machines = {MACHINE_ID: MACHINE, STORED_MACHINE.id: STORED_MACHINE}


def machine_from_id(id: int):
    return machines[id]


def test_handle_scan_data__upserts_machine(
    handler: handle_ping_scan_event,
    machine_repository: IMachineRepository,
):
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    handler(EVENT)

    expected_machine = STORED_MACHINE.copy()
    expected_machine.operating_system = OperatingSystem.LINUX

    assert machine_repository.upsert_machine.called_with(expected_machine)


def test_handle_scan_data__upserts_node(
    handler: handle_ping_scan_event,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
):
    machine_repository.get_machine_by_id = MagicMock(return_value=STORED_MACHINE)
    handler(EVENT)

    assert node_repository.upsert_communication.called_with(
        MACHINE.id, STORED_MACHINE.id, CommunicationType.SCANNED
    )


def test_handle_scan_data__node_not_upserted_if_no_matching_agent(
    handler: handle_ping_scan_event,
    agent_repository: IAgentRepository,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
):
    agent_repository.get_agent_by_id = MagicMock(side_effect=UnknownRecordError)
    machine_repository.get_machine_by_id = MagicMock(return_value=STORED_MACHINE)

    handler(EVENT)

    assert not node_repository.upsert_communication.called


def test_handle_scan_data__node_not_upserted_if_no_matching_machine(
    handler: handle_ping_scan_event,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
):
    machine_repository.get_machine_by_id = MagicMock(side_effect=UnknownRecordError)

    handler(EVENT)

    assert not node_repository.upsert_communication.called


def test_handle_scan_data__upserts_machine_if_not_existed(
    handler: handle_ping_scan_event, machine_repository: IMachineRepository
):
    machine_repository.get_machine_by_id = MagicMock(side_effect=machine_from_id)
    handler(EVENT)

    expected_machine = Machine(id=SEED_ID, operating_system=OperatingSystem.LINUX)

    assert machine_repository.upsert_machine.called_with(expected_machine)

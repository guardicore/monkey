from ipaddress import IPv4Address, IPv4Interface
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.monkey_island import InMemoryMachineRepository

from common.agent_events import AbstractAgentEvent
from common.types import AgentID, SocketAddress
from monkey_island.cc.agent_event_handlers.node_update_facade import NodeUpdateFacade
from monkey_island.cc.models import Agent, CommunicationType, Machine
from monkey_island.cc.repository import (
    IAgentRepository,
    IMachineRepository,
    INodeRepository,
    UnknownRecordError,
)


class TestEvent(AbstractAgentEvent):
    success: bool


SEED_ID = 99
SOURCE_IP_ADDRESS = IPv4Address("10.10.10.99")

SOURCE_MACHINE_ID = 1
SOURCE_MACHINE = Machine(
    id=SOURCE_MACHINE_ID,
    hardware_id=5,
    network_interfaces=[IPv4Interface(SOURCE_IP_ADDRESS)],
)

SOURCE_AGENT_ID = UUID("655fd01c-5eec-4e42-b6e3-1fb738c2978d")
SOURCE_AGENT = Agent(
    id=SOURCE_AGENT_ID,
    machine_id=SOURCE_MACHINE_ID,
    start_time=0,
    parent_id=None,
    cc_server=(SocketAddress(ip="10.10.10.10", port=5000)),
)

TARGET_IP_ADDRESS = IPv4Address("10.10.10.100")
TARGET_MACHINE_ID = 2
TARGET_MACHINE = Machine(
    id=TARGET_MACHINE_ID,
    hardware_id=5,
    network_interfaces=[IPv4Interface(TARGET_IP_ADDRESS)],
)
EXPECTED_CREATED_MACHINE = Machine(
    id=SEED_ID,
    network_interfaces=[IPv4Interface(SOURCE_IP_ADDRESS)],
)

TEST_EVENT = TestEvent(source=SOURCE_AGENT_ID, target=TARGET_IP_ADDRESS, success=True)


@pytest.fixture
def agent_repository() -> IAgentRepository:
    def get_agent_by_id(agent_id: AgentID) -> Agent:
        if agent_id == SOURCE_AGENT_ID:
            return SOURCE_AGENT

        raise UnknownRecordError()

    agent_repository = MagicMock(spec=IAgentRepository)
    agent_repository.get_agent_by_id = MagicMock(side_effect=get_agent_by_id)
    return agent_repository


@pytest.fixture
def machine_repository() -> IMachineRepository:
    machine_repository = InMemoryMachineRepository(SEED_ID)
    machine_repository.upsert_machine(SOURCE_MACHINE)
    machine_repository.upsert_machine(TARGET_MACHINE)

    return machine_repository


@pytest.fixture
def node_repository() -> INodeRepository:
    node_repository = MagicMock(spec=INodeRepository)
    return node_repository


@pytest.fixture
def node_update_facade(
    agent_repository: IAgentRepository,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
) -> NodeUpdateFacade:
    return NodeUpdateFacade(agent_repository, machine_repository, node_repository)


def test_return_existing_machine(node_update_facade, machine_repository):
    machine_repository.get_machines_by_ip = MagicMock(return_value=[SOURCE_MACHINE])

    target_machine = node_update_facade.get_or_create_target_machine(SOURCE_IP_ADDRESS)

    assert target_machine == SOURCE_MACHINE


def test_create_new_machine(node_update_facade, machine_repository):
    machine_repository.get_machines_by_ip = MagicMock(side_effect=UnknownRecordError)

    target_machine = node_update_facade.get_or_create_target_machine(SOURCE_IP_ADDRESS)

    assert target_machine == EXPECTED_CREATED_MACHINE
    assert machine_repository.get_machine_by_id(target_machine.id) == target_machine


def test_get_event_source_machine(node_update_facade):
    assert node_update_facade.get_event_source_machine(TEST_EVENT) == SOURCE_MACHINE


def test_upsert_communication_from_event__empty_node_repository(
    node_update_facade, node_repository
):
    node_update_facade.upsert_communication_from_event(TEST_EVENT, CommunicationType.SCANNED)

    node_repository.upsert_communication.assert_called_with(
        SOURCE_MACHINE_ID, TARGET_MACHINE_ID, CommunicationType.SCANNED
    )


def test_upsert_communication_from_event__no_target_ip(node_update_facade):
    event = TestEvent(source=SOURCE_AGENT_ID, target=None, success=True)

    with pytest.raises(TypeError):
        node_update_facade.upsert_communication_from_event(event, CommunicationType.SCANNED)

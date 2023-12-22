from ipaddress import IPv4Address, IPv4Interface
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from monkeyevents import AbstractAgentEvent
from monkeytypes import SocketAddress
from tests.monkey_island import InMemoryAgentRepository, InMemoryMachineRepository

from monkey_island.cc.models import Agent, CommunicationType, Machine
from monkey_island.cc.repositories import (
    AgentMachineFacade,
    IAgentRepository,
    IMachineRepository,
    INodeRepository,
    NetworkModelUpdateFacade,
    UnknownRecordError,
)


class FakeEvent(AbstractAgentEvent):
    success: bool


SEED_ID = 99
SOURCE_IP_ADDRESS = IPv4Address("10.10.10.99")

SOURCE_MACHINE_ID = 1
SOURCE_MACHINE = Machine(
    id=SOURCE_MACHINE_ID,
    hardware_id=5,
    network_interfaces=[IPv4Interface(SOURCE_IP_ADDRESS)],
)

AGENT_SHA256 = "0204d7e486443c17c30a822ac191feca4fcfd038b3a33d8227499a69828dca1f"
SOURCE_AGENT_ID = UUID("655fd01c-5eec-4e42-b6e3-1fb738c2978d")
SOURCE_AGENT = Agent(
    id=SOURCE_AGENT_ID,
    machine_id=SOURCE_MACHINE_ID,
    start_time=0,
    parent_id=None,
    cc_server=(SocketAddress(ip="10.10.10.10", port=5000)),
    sha256=AGENT_SHA256,
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

TEST_EVENT = FakeEvent(source=SOURCE_AGENT_ID, target=TARGET_IP_ADDRESS, success=True)


@pytest.fixture
def agent_repository() -> IAgentRepository:
    agent_repository = InMemoryAgentRepository()
    agent_repository.upsert_agent(SOURCE_AGENT)

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
def agent_machine_facade(
    agent_repository: IAgentRepository, machine_repository: IMachineRepository
) -> AgentMachineFacade:
    return AgentMachineFacade(agent_repository, machine_repository)


@pytest.fixture
def network_model_update_facade(
    agent_machine_facade: AgentMachineFacade,
    machine_repository: IMachineRepository,
    node_repository: INodeRepository,
) -> NetworkModelUpdateFacade:
    return NetworkModelUpdateFacade(agent_machine_facade, machine_repository, node_repository)


def test_return_existing_machine(network_model_update_facade, machine_repository):
    machine_repository.get_machines_by_ip = MagicMock(return_value=[SOURCE_MACHINE])

    target_machine = network_model_update_facade.get_or_create_target_machine(SOURCE_IP_ADDRESS)

    assert target_machine == SOURCE_MACHINE


def test_create_new_machine(network_model_update_facade, machine_repository):
    machine_repository.get_machines_by_ip = MagicMock(side_effect=UnknownRecordError)

    target_machine = network_model_update_facade.get_or_create_target_machine(SOURCE_IP_ADDRESS)

    assert target_machine == EXPECTED_CREATED_MACHINE
    assert machine_repository.get_machine_by_id(target_machine.id) == target_machine


def test_upsert_communication_from_event(network_model_update_facade, node_repository):
    network_model_update_facade.upsert_communication_from_event(
        TEST_EVENT, CommunicationType.SCANNED
    )

    node_repository.upsert_communication.assert_called_with(
        SOURCE_MACHINE_ID, TARGET_MACHINE_ID, CommunicationType.SCANNED
    )


def test_upsert_communication_from_event__no_target_ip(network_model_update_facade):
    event = FakeEvent(source=SOURCE_AGENT_ID, target=None, success=True)

    with pytest.raises(TypeError):
        network_model_update_facade.upsert_communication_from_event(
            event, CommunicationType.SCANNED
        )


def test_cache_reset__get_or_create_target_machine(network_model_update_facade, machine_repository):
    original_target = network_model_update_facade.get_or_create_target_machine(TARGET_IP_ADDRESS)
    original_target_machine_no_interfaces = TARGET_MACHINE.copy()
    original_target_machine_no_interfaces.network_interfaces = []
    machine_repository.upsert_machine(original_target_machine_no_interfaces)

    network_model_update_facade.reset_cache()
    new_target = network_model_update_facade.get_or_create_target_machine(TARGET_IP_ADDRESS)

    assert original_target.id != new_target.id

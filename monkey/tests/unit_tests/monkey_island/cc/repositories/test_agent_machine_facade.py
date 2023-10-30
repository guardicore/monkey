from copy import deepcopy
from ipaddress import IPv4Address, IPv4Interface
from uuid import UUID

import pytest
from monkeytypes import SocketAddress
from tests.monkey_island import InMemoryAgentRepository, InMemoryMachineRepository

from monkey_island.cc.models import Agent, Machine
from monkey_island.cc.repositories import AgentMachineFacade, IAgentRepository, IMachineRepository

SEED_ID = 99
SOURCE_IP_ADDRESS = IPv4Address("10.10.10.99")

SOURCE_MACHINE_ID = 1
SOURCE_MACHINE = Machine(
    id=SOURCE_MACHINE_ID,
    hardware_id=5,
    network_interfaces=[IPv4Interface(SOURCE_IP_ADDRESS)],
)

AGENT_ID = UUID("655fd01c-5eec-4e42-b6e3-1fb738c2978d")
AGENT_SHA256 = "5d1bb53850d782d42b0b9d86497ca95986d4945d3284a0e5fc0f7beaccde19c6"
AGENT = Agent(
    id=AGENT_ID,
    machine_id=SOURCE_MACHINE_ID,
    start_time=0,
    parent_id=None,
    cc_server=(SocketAddress(ip="10.10.10.10", port=5000)),
    sha256=AGENT_SHA256,
)


@pytest.fixture
def agent_repository() -> IAgentRepository:
    agent_repository = InMemoryAgentRepository()
    agent_repository.upsert_agent(AGENT)

    return agent_repository


@pytest.fixture
def machine_repository() -> IMachineRepository:
    machine_repository = InMemoryMachineRepository(SEED_ID)
    machine_repository.upsert_machine(SOURCE_MACHINE)

    return machine_repository


@pytest.fixture
def agent_machine_facade(agent_repository, machine_repository) -> AgentMachineFacade:
    return AgentMachineFacade(agent_repository, machine_repository)


def test_get_machine_id_from_agent_id(agent_machine_facade):
    assert agent_machine_facade.get_machine_id_from_agent_id(AGENT_ID) == SOURCE_MACHINE_ID


def test_cache_reset__get_machine_id_from_agent_id(
    agent_machine_facade, agent_repository, machine_repository
):
    original_machine_id = agent_machine_facade.get_machine_id_from_agent_id(AGENT_ID)
    new_machine_id = original_machine_id + 100
    new_machine = Machine(
        id=new_machine_id,
        hardware_id=5,
        network_interfaces=[IPv4Interface(SOURCE_IP_ADDRESS)],
    )
    machine_repository.upsert_machine(new_machine)
    new_agent = Agent(
        id=AGENT_ID,
        machine_id=new_machine_id,
        start_time=0,
        parent_id=None,
        cc_server=(SocketAddress(ip="10.10.10.10", port=5000)),
        sha256=AGENT_SHA256,
    )

    agent_repository.reset()
    agent_repository.upsert_agent(new_agent)
    agent_machine_facade.reset_cache()
    new_machine_id = agent_machine_facade.get_machine_id_from_agent_id(AGENT_ID)

    assert original_machine_id != new_machine_id


def test_get_agent_machine(agent_machine_facade):
    assert agent_machine_facade.get_agent_machine(AGENT_ID) == SOURCE_MACHINE


def test_upsert_machine(agent_machine_facade, machine_repository):
    new_machine = deepcopy(SOURCE_MACHINE)
    new_machine.hostname = "blah"

    agent_machine_facade.upsert_machine(new_machine)

    machines = machine_repository.get_machines()
    assert list(machines) == [new_machine]

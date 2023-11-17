from ipaddress import IPv4Interface
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from monkeyevents import OSDiscoveryEvent
from monkeytypes import OperatingSystem, SocketAddress
from tests.monkey_island import InMemoryMachineRepository

from monkey_island.cc.agent_event_handlers import update_machine_os
from monkey_island.cc.models import Agent, Machine
from monkey_island.cc.repositories import (
    AgentMachineFacade,
    IAgentRepository,
    IMachineRepository,
    UnknownRecordError,
)

# The machine
SEED_ID = 1
MACHINE_ID = 99
MACHINE = Machine(
    id=MACHINE_ID,
    hardware_id=33,
    operating_system=None,
    operating_system_version="",
    network_interfaces=[IPv4Interface("10.10.10.55/24")],
)

# The agent
AGENT_ID = UUID("72a64013-b3ab-4be9-9f05-0ffaccf01950")
AGENT_SHA256 = "142e6b8c77382ebaa41d3eb5cc6520dc5922d1030ecf2fa6fbb9b2462af11bbe"
CC_SERVER = SocketAddress(ip="10.10.10.100", port="5000")
AGENT = Agent(
    id=AGENT_ID, machine_id=MACHINE_ID, start_time=0, cc_server=CC_SERVER, sha256=AGENT_SHA256
)

# The event
EVENT = OSDiscoveryEvent(source=AGENT_ID, os=OperatingSystem.LINUX, version="blah")


@pytest.fixture
def agent_repository() -> IAgentRepository:
    repository = MagicMock(spec=IAgentRepository)
    repository.get_agent_by_id = MagicMock(return_value=AGENT)
    return repository


MACHINES_BY_ID = {MACHINE_ID: MACHINE}


def machine_from_id(id):
    return MACHINES_BY_ID[id]


@pytest.fixture
def machine_repository() -> IMachineRepository:
    repository = InMemoryMachineRepository(SEED_ID)
    repository.upsert_machine(MACHINE)
    return repository


@pytest.fixture
def agent_machine_facade(agent_repository, machine_repository) -> AgentMachineFacade:
    return AgentMachineFacade(agent_repository, machine_repository)


@pytest.fixture
def updater(agent_machine_facade) -> update_machine_os:
    return update_machine_os(agent_machine_facade)


def test_machine_updated(updater, machine_repository):
    updater(EVENT)

    machine = machine_repository.get_machines()[0]
    assert machine.operating_system == EVENT.os
    assert machine.operating_system_version == EVENT.version


def test_machine_not_updated_if_no_agent(updater, agent_repository, machine_repository):
    agent_repository.get_agent_by_id = MagicMock(side_effect=UnknownRecordError)

    with pytest.raises(UnknownRecordError):
        updater(EVENT)

    machines = machine_repository.get_machines()
    assert list(machines) == [MACHINE]


def test_machine_not_updated_if_no_machine(updater, machine_repository):
    machine_repository.reset()

    with pytest.raises(UnknownRecordError):
        updater(EVENT)

    assert not machine_repository.get_machines()

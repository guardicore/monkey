from ipaddress import IPv4Address, IPv4Interface
from unittest.mock import MagicMock

import pytest

from monkey_island.cc.agent_event_handlers.node_update_facade import NodeUpdateFacade
from monkey_island.cc.models import Machine
from monkey_island.cc.repository import IMachineRepository, UnknownRecordError

SEED_ID = 99
IP_ADDRESS = IPv4Address("10.10.10.99")

EXISTING_MACHINE = Machine(
    id=1,
    hardware_id=5,
    network_interfaces=[IPv4Interface(IP_ADDRESS)],
)

EXPECTED_CREATED_MACHINE = Machine(
    id=SEED_ID,
    network_interfaces=[IPv4Interface(IP_ADDRESS)],
)


@pytest.fixture
def machine_repository() -> IMachineRepository:
    machine_repository = MagicMock(spec=IMachineRepository)
    machine_repository.get_new_id = MagicMock(return_value=SEED_ID)
    return machine_repository


@pytest.fixture
def node_update_facade(machine_repository) -> NodeUpdateFacade:
    return NodeUpdateFacade(machine_repository)


def test_return_existing_machine(node_update_facade, machine_repository):
    machine_repository.get_machines_by_ip = MagicMock(return_value=[EXISTING_MACHINE])

    target_machine = node_update_facade.get_or_create_target_machine(IP_ADDRESS)

    assert target_machine == EXISTING_MACHINE


def test_create_new_machine(node_update_facade, machine_repository):
    machine_repository.get_machines_by_ip = MagicMock(side_effect=UnknownRecordError)

    target_machine = node_update_facade.get_or_create_target_machine(IP_ADDRESS)

    assert target_machine == EXPECTED_CREATED_MACHINE
    assert machine_repository.upsert_machine.called_once_with(target_machine)

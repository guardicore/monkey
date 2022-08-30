from ipaddress import IPv4Interface
from itertools import chain, repeat
from unittest.mock import MagicMock

import mongomock
import pytest

from common import OperatingSystem
from monkey_island.cc.models import Machine
from monkey_island.cc.repository import (
    IMachineRepository,
    MongoMachineRepository,
    RemovalError,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)

MACHINES = (
    Machine(
        id=1,
        hardware_id=12345,
        network_interfaces=[IPv4Interface("192.168.1.10/24")],
        operating_system=OperatingSystem.LINUX,
        operating_system_version="Ubuntu 22.04",
        hostname="wopr",
    ),
    Machine(
        id=2,
        hardware_id=67890,
        network_interfaces=[IPv4Interface("192.168.1.11/24"), IPv4Interface("192.168.1.12/24")],
        operating_system=OperatingSystem.WINDOWS,
        operating_system_version="eXtra Problems",
        hostname="hal",
    ),
    Machine(
        id=3,
        hardware_id=112345,
        network_interfaces=[IPv4Interface("192.168.1.13/24"), IPv4Interface("192.168.1.14/24")],
        operating_system=OperatingSystem.WINDOWS,
        operating_system_version="Vista",
        hostname="smith",
    ),
    Machine(
        id=4,
        hardware_id=167890,
        network_interfaces=[IPv4Interface("192.168.1.14/24")],
        operating_system=OperatingSystem.LINUX,
        operating_system_version="CentOS Linux 8",
        hostname="skynet",
    ),
)


@pytest.fixture
def mongo_client() -> mongomock.MongoClient:
    client = mongomock.MongoClient()
    client.monkey_island.machines.insert_many((m.dict(simplify=True) for m in MACHINES))
    return client


@pytest.fixture
def error_raising_mock_mongo_client() -> mongomock.MongoClient:
    mongo_client = MagicMock(spec=mongomock.MongoClient)
    mongo_client.monkey_island = MagicMock(spec=mongomock.Database)
    mongo_client.monkey_island.machines = MagicMock(spec=mongomock.Collection)

    # The first call to find() must succeed
    mongo_client.monkey_island.machines.find = MagicMock(
        side_effect=chain([MagicMock()], repeat(Exception("some exception")))
    )
    mongo_client.monkey_island.machines.find_one = MagicMock(
        side_effect=Exception("some exception")
    )
    mongo_client.monkey_island.machines.insert_one = MagicMock(
        side_effect=Exception("some exception")
    )
    mongo_client.monkey_island.machines.replace_one = MagicMock(
        side_effect=Exception("some exception")
    )
    mongo_client.monkey_island.machines.drop = MagicMock(side_effect=Exception("some exception"))

    return mongo_client


@pytest.fixture
def error_raising_machine_repository(error_raising_mock_mongo_client) -> IMachineRepository:
    return MongoMachineRepository(error_raising_mock_mongo_client)


@pytest.fixture
def machine_repository(mongo_client) -> IMachineRepository:
    return MongoMachineRepository(mongo_client)


def test_create_machine__unique_id(machine_repository):
    new_machine = machine_repository.create_machine()

    for m in MACHINES:
        assert m.id != new_machine.id


def test_create_machine__multiple_unique_ids(machine_repository):
    new_machine_1 = machine_repository.create_machine()
    new_machine_2 = machine_repository.create_machine()

    assert new_machine_1.id != new_machine_2.id


def test_create_machine__new_id_for_empty_repo(machine_repository):
    empty_machine_repository = MongoMachineRepository(mongomock.MongoClient())
    new_machine_1 = empty_machine_repository.create_machine()
    new_machine_2 = empty_machine_repository.create_machine()

    assert new_machine_1.id != new_machine_2.id


def test_create_machine__storage_error(error_raising_machine_repository):
    with pytest.raises(StorageError):
        error_raising_machine_repository.create_machine()


def test_update_machine(machine_repository):
    machine = machine_repository.get_machine_by_id(1)

    machine.operating_system = OperatingSystem.WINDOWS
    machine.hostname = "viki"
    machine.network_interfaces = [IPv4Interface("10.0.0.1/16")]

    machine_repository.update_machine(machine)

    assert machine_repository.get_machine_by_id(1) == machine


def test_update_machine__not_found(machine_repository):
    machine = Machine(id=99)

    with pytest.raises(UnknownRecordError):
        machine_repository.update_machine(machine)


def test_update_machine__storage_error_exception(error_raising_machine_repository):
    machine = MACHINES[0]

    with pytest.raises(StorageError):
        error_raising_machine_repository.update_machine(machine)


def test_update_machine__storage_error_update_failed(error_raising_mock_mongo_client):
    mock_result = MagicMock()
    mock_result.matched_count = 1
    mock_result.modified_count = 0

    error_raising_mock_mongo_client.monkey_island.machines.replace_one = MagicMock(
        return_value=mock_result
    )
    machine_repository = MongoMachineRepository(error_raising_mock_mongo_client)

    machine = MACHINES[0]
    with pytest.raises(StorageError):
        machine_repository.update_machine(machine)


def test_get_machine_by_id(machine_repository):
    for i, expected_machine in enumerate(MACHINES, start=1):
        assert machine_repository.get_machine_by_id(i) == expected_machine


def test_get_machine_by_id__not_found(machine_repository):
    with pytest.raises(UnknownRecordError):
        machine_repository.get_machine_by_id(9999)


def test_get_machine_by_id__retrieval_error(error_raising_machine_repository):
    with pytest.raises(RetrievalError):
        error_raising_machine_repository.get_machine_by_id(1)


def test_get_machine_by_hardware_id(machine_repository):
    for hardware_id, expected_machine in ((machine.hardware_id, machine) for machine in MACHINES):
        assert machine_repository.get_machine_by_hardware_id(hardware_id) == expected_machine


def test_get_machine_by_hardware_id__not_found(machine_repository):
    with pytest.raises(UnknownRecordError):
        machine_repository.get_machine_by_hardware_id(9999888887777)


def test_get_machine_by_hardware_id__retrieval_error(error_raising_machine_repository):
    with pytest.raises(RetrievalError):
        error_raising_machine_repository.get_machine_by_hardware_id(1)


def test_get_machine_by_ip(machine_repository):
    expected_machine = MACHINES[0]
    expected_machine_ip = expected_machine.network_interfaces[0].ip

    retrieved_machines = machine_repository.get_machines_by_ip(expected_machine_ip)

    assert len(retrieved_machines) == 1
    assert retrieved_machines[0] == expected_machine


def test_get_machine_by_ip__multiple_results(machine_repository):
    search_ip = MACHINES[3].network_interfaces[0].ip

    retrieved_machines = machine_repository.get_machines_by_ip(search_ip)

    assert len(retrieved_machines) == 2
    assert MACHINES[2] in retrieved_machines
    assert MACHINES[3] in retrieved_machines


def test_get_machine_by_ip__not_found(machine_repository):
    with pytest.raises(UnknownRecordError):
        machine_repository.get_machines_by_ip("1.1.1.1")


def test_get_machine_by_ip__retrieval_error(error_raising_machine_repository):
    with pytest.raises(RetrievalError):
        error_raising_machine_repository.get_machines_by_ip("1.1.1.1")


def test_reset(machine_repository):
    # Ensure the repository is not empty
    preexisting_machine = machine_repository.get_machine_by_id(MACHINES[0].id)
    assert isinstance(preexisting_machine, Machine)

    machine_repository.reset()

    with pytest.raises(UnknownRecordError):
        machine_repository.get_machine_by_id(MACHINES[0].id)


def test_usable_after_reset(machine_repository):
    machine_repository.reset()

    new_machine = machine_repository.create_machine()

    assert new_machine == machine_repository.get_machine_by_id(new_machine.id)


def test_reset__removal_error(error_raising_machine_repository):
    with pytest.raises(RemovalError):
        error_raising_machine_repository.reset()

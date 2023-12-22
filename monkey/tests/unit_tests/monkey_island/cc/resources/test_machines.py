from http import HTTPStatus
from ipaddress import IPv4Interface
from unittest.mock import MagicMock

import pytest
from monkeytypes import OperatingSystem
from tests.common import StubDIContainer
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.models import Machine
from monkey_island.cc.repositories import IMachineRepository, RetrievalError
from monkey_island.cc.resources import Machines

MACHINES_URL = get_url_for_resource(Machines)
MACHINES = [
    Machine(
        id=1,
        hardware_id=101,
        island=True,
        network_interfaces=[IPv4Interface("10.10.10.1")],
        operating_system=OperatingSystem.WINDOWS,
    ),
    Machine(
        id=2,
        hardware_id=102,
        island=False,
        network_interfaces=[IPv4Interface("10.10.10.2/24")],
        operating_system=OperatingSystem.LINUX,
    ),
]


@pytest.fixture
def mock_machine_repository() -> IMachineRepository:
    machine_repository = MagicMock(spec=IMachineRepository)
    return machine_repository


@pytest.fixture
def flask_client(build_flask_client, mock_machine_repository):
    container = StubDIContainer()

    container.register_instance(IMachineRepository, mock_machine_repository)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_machines_get__status_ok(flask_client, mock_machine_repository):
    mock_machine_repository.get_machines = MagicMock(return_value=MACHINES)

    resp = flask_client.get(MACHINES_URL)

    assert resp.status_code == HTTPStatus.OK


def test_machines_get__gets_machines(flask_client, mock_machine_repository):
    mock_machine_repository.get_machines = MagicMock(return_value=MACHINES)

    resp = flask_client.get(MACHINES_URL)

    response_machines = [Machine(**m) for m in resp.json]
    for machine in response_machines:
        assert machine in MACHINES


def test_machines_get__gets_no_machines(flask_client, mock_machine_repository):
    mock_machine_repository.get_machines = MagicMock(return_value=[])

    resp = flask_client.get(MACHINES_URL)

    assert resp.json == []


def test_machines_get__retrieval_error(flask_client, mock_machine_repository):
    mock_machine_repository.get_machines = MagicMock(side_effect=RetrievalError)

    resp = flask_client.get(MACHINES_URL)

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

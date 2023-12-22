from http import HTTPStatus
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from monkeytypes import SocketAddress
from tests.common import StubDIContainer
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.event_queue import IIslandEventQueue
from monkey_island.cc.models import Agent
from monkey_island.cc.repositories import IAgentRepository
from monkey_island.cc.resources import Agents

AGENT_REGISTRATION_DICT = {
    "id": UUID("6bfd8b64-43d8-4449-8c70-d898aca74ad8"),
    "machine_hardware_id": 1,
    "start_time": 0,
    "parent_id": UUID("9d55ba33-95c2-417d-bd86-d3d11e47daeb"),
    "cc_server": {"ip": "10.0.0.1", "port": "5000"},
    "network_interfaces": ["10.1.1.2/24"],
    "sha256": "cf5c10a8073aa923877ee66df8c1912cac2dbb4b85a97d09cb95d57bde4d2876",
}

AGENT_SHA256 = "7ac0f5c62a9bcb81af3e9d67a764d7bbd3cce9af7cd26c211f136400ebe703c4"
AGENTS = (
    Agent(
        id=UUID("12345678-1234-1234-1234-123456789abc"),
        machine_id=2,
        start_time=0,
        stop_time=10,
        cc_server=SocketAddress(ip="10.0.0.1", port=5000),
        sha256=AGENT_SHA256,
    ),
    Agent(
        id=UUID("abcdef78-abcd-abcd-abcd-abcdef123456"),
        machine_id=3,
        start_time=5,
        stop_time=15,
        cc_server=SocketAddress(ip="10.0.0.1", port=5000),
        sha256=AGENT_SHA256,
    ),
)


@pytest.fixture
def agent_repository() -> IAgentRepository:
    agent_repository = MagicMock(spec=IAgentRepository)
    agent_repository.get_agents = MagicMock(return_value=AGENTS)

    return agent_repository


@pytest.fixture
def flask_client(build_flask_client, agent_repository):
    container = StubDIContainer()
    container.register_instance(IIslandEventQueue, MagicMock(spec=IIslandEventQueue))
    container.register_instance(IAgentRepository, agent_repository)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_agent_registration(flask_client):
    resp = flask_client.post(
        get_url_for_resource(Agents),
        json=AGENT_REGISTRATION_DICT,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_agent_registration_invalid_data(flask_client):
    agent_registration_dict = AGENT_REGISTRATION_DICT.copy()

    agent_registration_dict["id"] = 1

    resp = flask_client.post(
        get_url_for_resource(Agents),
        json=agent_registration_dict,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.BAD_REQUEST


def test_get_agents__status_code(flask_client):
    resp = flask_client.get(
        get_url_for_resource(Agents),
        follow_redirects=True,
    )
    assert resp.status_code == HTTPStatus.OK


def test_get_agents__data(flask_client):
    resp = flask_client.get(
        get_url_for_resource(Agents),
        follow_redirects=True,
    )

    agents = [Agent(**a) for a in resp.json]
    assert len(agents) == len(AGENTS)
    for a in agents:
        assert a in AGENTS

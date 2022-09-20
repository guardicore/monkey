from http import HTTPStatus
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.common import StubDIContainer
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.event_queue import IIslandEventQueue
from monkey_island.cc.resources import Agents

AGENTS_URL = get_url_for_resource(Agents)

AGENT_REGISTRATION_DICT = {
    "id": UUID("6bfd8b64-43d8-4449-8c70-d898aca74ad8"),
    "machine_hardware_id": 1,
    "start_time": 0,
    "parent_id": UUID("9d55ba33-95c2-417d-bd86-d3d11e47daeb"),
    "cc_server": "10.0.0.1:5000",
    "network_interfaces": ["10.1.1.2/24"],
}


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()
    container.register_instance(IIslandEventQueue, MagicMock(spec=IIslandEventQueue))

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_agent_registration(flask_client):
    print(AGENTS_URL)
    resp = flask_client.post(
        AGENTS_URL,
        json=AGENT_REGISTRATION_DICT,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_agent_registration_invalid_data(flask_client):
    agent_registration_dict = AGENT_REGISTRATION_DICT.copy()

    agent_registration_dict["id"] = 1

    resp = flask_client.post(
        AGENTS_URL,
        json=agent_registration_dict,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.BAD_REQUEST

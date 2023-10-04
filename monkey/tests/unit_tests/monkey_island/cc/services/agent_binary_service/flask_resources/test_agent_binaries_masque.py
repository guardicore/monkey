from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from monkeytypes import OperatingSystem
from tests.common import StubDIContainer
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.services import IAgentBinaryService
from monkey_island.cc.services.agent_binary_service.flask_resources.agent_binaries_masque import (
    AgentBinariesMasque,
)

LINUX = "linux"
WINDOWS = "windows"
UNRECOGNIZED = "unrecognized"

LINUX_MASQUE = b"linux-masque\xBE\xEF\x00\xFA\xCE"
WINDOWS_MASQUE = b"windows-masque\x0F\xF1\xCE\x00\xBA\xBB\x1E"


@pytest.fixture
def agent_binary_service() -> IAgentBinaryService:
    agent_binary_service = MagicMock(spec=IAgentBinaryService)

    return agent_binary_service


@pytest.fixture
def flask_client(build_flask_client, agent_binary_service):
    container = StubDIContainer()
    container.register_instance(IAgentBinaryService, agent_binary_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


@pytest.mark.parametrize(
    "operating_system, masque", [(LINUX, LINUX_MASQUE), (WINDOWS, WINDOWS_MASQUE), (LINUX, b"")]
)
def test_get_masque(agent_binary_service, flask_client, operating_system, masque):
    agent_binary_service.get_masque = MagicMock(return_value=masque)

    resp = flask_client.get(
        get_url_for_resource(AgentBinariesMasque, os=operating_system),
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.data == masque


def test_get_masque__none_value(flask_client):
    agent_binary_service.get_masque = MagicMock(return_value=None)

    resp = flask_client.get(
        get_url_for_resource(AgentBinariesMasque, os=LINUX),
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.data == b""


def test_get_masque__unrecognized_operating_system(flask_client):
    resp = flask_client.get(
        get_url_for_resource(AgentBinariesMasque, os=UNRECOGNIZED),
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "operating_system, masque",
    [
        (LINUX, LINUX_MASQUE),
        (WINDOWS, WINDOWS_MASQUE),
        (LINUX, b""),
        (WINDOWS, "just a string"),
    ],
)
def test_set_masque(flask_client, operating_system, masque):
    resp = flask_client.put(
        get_url_for_resource(AgentBinariesMasque, os=operating_system),
        data=masque,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.NO_CONTENT


def test_set_masque__unrecognized_operating_system(flask_client):
    resp = flask_client.put(
        get_url_for_resource(AgentBinariesMasque, os=UNRECOGNIZED),
        data=LINUX_MASQUE,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND


def test_set_masque__empty(agent_binary_service, flask_client):
    resp = flask_client.put(
        get_url_for_resource(AgentBinariesMasque, os="linux"),
        data=b"",
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.NO_CONTENT
    agent_binary_service.set_masque.assert_called_with(OperatingSystem.LINUX, None)

from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from common.agent_plugins import AgentPluginType, PluginVersion
from monkey_island.cc.repositories import RetrievalError, StorageError
from monkey_island.cc.services import IAgentPluginService
from monkey_island.cc.services.agent_plugin_service.errors import PluginInstallationError
from monkey_island.cc.services.agent_plugin_service.flask_resources.install_agent_plugin import (  # noqa: E501
    InstallAgentPlugin,
)

AGENT_PLUGIN = b"SomePlugin"
PLUGIN_TYPE = "Exploiter"
PLUGIN_NAME = "RDP"
VERSION_DICT = {"major": "1", "minor": "0", "patch": "1"}
VERSION = "1.0.1"
REQUEST_JSON_DATA = (
    f'{{"plugin_type": "{PLUGIN_TYPE}", "name": "{PLUGIN_NAME}", "version": "{VERSION}"}}'
)


@pytest.fixture
def agent_plugin_service() -> IAgentPluginService:
    return MagicMock(spec=IAgentPluginService)


@pytest.fixture
def flask_client(build_flask_client, agent_plugin_service):
    container = StubDIContainer()
    container.register_instance(IAgentPluginService, agent_plugin_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_install_plugin__binary(agent_plugin_service, flask_client):
    resp = flask_client.put(
        get_url_for_resource(InstallAgentPlugin),
        data=AGENT_PLUGIN,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.OK
    assert agent_plugin_service.install_plugin_from_repository.call_count == 0
    assert agent_plugin_service.install_plugin_archive.call_count == 1
    assert agent_plugin_service.install_plugin_archive.call_args[0][0] == AGENT_PLUGIN


def test_install_plugin__json(agent_plugin_service, flask_client):
    resp = flask_client.put(
        get_url_for_resource(InstallAgentPlugin),
        data=REQUEST_JSON_DATA,
        follow_redirects=True,
        headers={"Content-Type": "application/json"},
    )

    assert resp.status_code == HTTPStatus.OK
    assert agent_plugin_service.install_plugin_archive.call_count == 0
    assert agent_plugin_service.install_plugin_from_repository.call_count == 1
    agent_plugin_service.install_plugin_from_repository.assert_called_with(
        plugin_type=AgentPluginType(PLUGIN_TYPE),
        plugin_name=PLUGIN_NAME,
        plugin_version=PluginVersion.from_str(VERSION),
    )


def test_install_plugin__binary_install_error(agent_plugin_service, flask_client):
    agent_plugin_service.install_plugin_archive = MagicMock(side_effect=PluginInstallationError)
    resp = flask_client.put(
        get_url_for_resource(InstallAgentPlugin),
        data=AGENT_PLUGIN,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_install_plugin__json_install_error(agent_plugin_service, flask_client):
    agent_plugin_service.install_plugin_from_repository = MagicMock(
        side_effect=PluginInstallationError
    )
    resp = flask_client.put(
        get_url_for_resource(InstallAgentPlugin),
        data=REQUEST_JSON_DATA,
        follow_redirects=True,
        headers={"Content-Type": "application/json"},
    )

    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("error", [RetrievalError, StorageError, Exception])
def test_install_plugin__binary_internal_server_error(agent_plugin_service, flask_client, error):
    agent_plugin_service.install_plugin_archive = MagicMock(side_effect=error)
    resp = flask_client.put(
        get_url_for_resource(InstallAgentPlugin),
        data=AGENT_PLUGIN,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.parametrize("error", [RetrievalError, StorageError, Exception])
def test_install_plugin__json_internal_server_error(agent_plugin_service, flask_client, error):
    agent_plugin_service.install_plugin_from_repository = MagicMock(side_effect=error)
    resp = flask_client.put(
        get_url_for_resource(InstallAgentPlugin),
        data=REQUEST_JSON_DATA,
        follow_redirects=True,
        headers={"Content-Type": "application/json"},
    )

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.parametrize(
    "request_data", [b"{}", None, "string", b'{"bogus":"vogus"', b'{"bogus": "bogus"}']
)
def test_install_plugin__json_bad_request(agent_plugin_service, flask_client, request_data):
    resp = flask_client.put(
        get_url_for_resource(InstallAgentPlugin),
        data=request_data,
        follow_redirects=True,
        headers={"Content-Type": "application/json"},
    )

    assert resp.status_code == HTTPStatus.BAD_REQUEST

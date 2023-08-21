from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.repositories import RetrievalError, StorageError
from monkey_island.cc.services import IAgentPluginService
from monkey_island.cc.services.agent_plugin_service.errors import PluginInstallationError
from monkey_island.cc.services.agent_plugin_service.flask_resources.install_agent_plugin import (  # noqa: E501
    InstallAgentPlugin,
)

AGENT_PLUGIN = b"SomePlugin"


@pytest.fixture
def agent_plugin_service() -> IAgentPluginService:
    return MagicMock(spec=IAgentPluginService)


@pytest.fixture
def flask_client(build_flask_client, agent_plugin_service):
    container = StubDIContainer()
    container.register_instance(IAgentPluginService, agent_plugin_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_install_plugin(agent_plugin_service, flask_client):
    resp = flask_client.put(
        get_url_for_resource(InstallAgentPlugin),
        data=AGENT_PLUGIN,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.OK
    assert agent_plugin_service.install_agent_plugin_archive.call_count == 1
    assert agent_plugin_service.install_agent_plugin_archive.call_args[0][0] == AGENT_PLUGIN


def test_install_plugin__install_error(agent_plugin_service, flask_client):
    agent_plugin_service.install_agent_plugin_archive = MagicMock(
        side_effect=PluginInstallationError
    )
    resp = flask_client.put(
        get_url_for_resource(InstallAgentPlugin),
        data=AGENT_PLUGIN,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("error", [RetrievalError, StorageError, Exception])
def test_install_plugin__internal_server_error(agent_plugin_service, flask_client, error):
    agent_plugin_service.install_agent_plugin_archive = MagicMock(side_effect=error)
    resp = flask_client.put(
        get_url_for_resource(InstallAgentPlugin),
        data=AGENT_PLUGIN,
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

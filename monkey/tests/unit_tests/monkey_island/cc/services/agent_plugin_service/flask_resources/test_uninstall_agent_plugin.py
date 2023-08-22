from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_TYPE
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import FAKE_AGENT_PLUGIN_1
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from common.agent_plugins import AgentPluginType
from monkey_island.cc.services.agent_plugin_service import IAgentPluginService
from monkey_island.cc.services.agent_plugin_service.errors import PluginUninstallationError
from monkey_island.cc.services.agent_plugin_service.flask_resources import UninstallAgentPlugin

REQUEST_DATA = (
    f'{{"plugin_type": "{FAKE_TYPE}", "name": "{FAKE_AGENT_PLUGIN_1.plugin_manifest.name}"}}'
)


@pytest.fixture
def agent_plugin_service():
    return MagicMock(spec=IAgentPluginService)


@pytest.fixture
def flask_client(build_flask_client, agent_plugin_service):
    container = StubDIContainer()
    container.register_instance(IAgentPluginService, agent_plugin_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_uninstall_agent_plugin(flask_client, agent_plugin_service):
    resp = flask_client.post(
        get_url_for_resource(UninstallAgentPlugin),
        data=REQUEST_DATA,
    )

    assert resp.status_code == HTTPStatus.OK
    agent_plugin_service.uninstall_agent_plugin.assert_called_with(
        AgentPluginType(FAKE_TYPE), FAKE_AGENT_PLUGIN_1.plugin_manifest.name
    )


@pytest.mark.parametrize(
    "type_",
    ["DummyType", "ExploiteR"],
)
def test_uninstall_agent_plugin__bad_request_if_type_is_invalid(
    flask_client, type_, agent_plugin_service
):
    resp = flask_client.post(
        get_url_for_resource(UninstallAgentPlugin),
        data=f'{{"plugin_type": "{type_}", "name": "name"}}',
    )

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    agent_plugin_service.uninstall_agent_plugin.assert_not_called()


@pytest.mark.parametrize("error", [Exception, PluginUninstallationError])
def test_uninstall_agent_plugin__error(flask_client, agent_plugin_service, error):
    def raise_error(plugin_type, name):
        raise error

    agent_plugin_service.uninstall_agent_plugin = raise_error

    resp = flask_client.post(
        get_url_for_resource(UninstallAgentPlugin),
        data=b'{"plugin_type": "Payload", "name": "name"}',
    )

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.parametrize(
    "request_data", [b"{}", None, "string", b'{"bogus":"vogus"', b'{"bogus": "bogus"}']
)
def test_uninstall_agent_plugin__bad_request_data(request_data, flask_client, agent_plugin_service):
    resp = flask_client.post(get_url_for_resource(UninstallAgentPlugin), data=request_data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    agent_plugin_service.uninstall_agent_plugin.assert_not_called()

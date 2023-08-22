from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_TYPE
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import FAKE_AGENT_PLUGIN_1
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from common.agent_plugins import AgentPluginType
from monkey_island.cc.repositories import RemovalError
from monkey_island.cc.services.agent_plugin_service import IAgentPluginService
from monkey_island.cc.services.agent_plugin_service.flask_resources import UninstallAgentPlugin


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
        get_url_for_resource(
            UninstallAgentPlugin,
            plugin_type=FAKE_TYPE,
            name=FAKE_AGENT_PLUGIN_1.plugin_manifest.name,
        )
    )

    assert resp.status_code == HTTPStatus.OK
    agent_plugin_service.uninstall_agent_plugin.assert_called_with(
        AgentPluginType(FAKE_TYPE), FAKE_AGENT_PLUGIN_1.plugin_manifest.name
    )


# TODO: Ask do we need some kind of UninstallAgentPluginError which will be handled
# if we can't uninstall a AgentPlugin
# def test_uninstall_agent_plugin_not_found_if_name_does_not_exist(flask_client):
#    resp = flask_client.post(
#        get_url_for_resource(UninstallAgentPlugin, plugin_type="Payload", name="name")
#    )
#
#    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "type_",
    ["DummyType", "ExploiteR"],
)
def test_uninstall_agent_plugin__not_found_if_type_is_invalid(
    flask_client, type_, agent_plugin_service
):
    resp = flask_client.post(
        get_url_for_resource(UninstallAgentPlugin, plugin_type=type_, name="name")
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND
    agent_plugin_service.uninstall_agent_plugin.assert_not_called()


def test_uninstall_agent_plugin__server_error(flask_client, agent_plugin_service):
    def raise_removal_error(plugin_type, name):
        raise RemovalError

    agent_plugin_service.uninstall_agent_plugin = raise_removal_error

    resp = flask_client.post(
        get_url_for_resource(UninstallAgentPlugin, plugin_type="Payload", name="name")
    )

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

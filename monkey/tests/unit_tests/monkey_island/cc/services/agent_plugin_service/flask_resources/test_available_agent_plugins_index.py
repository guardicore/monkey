from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from common.agent_plugins import AgentPluginRepositoryIndex
from monkey_island.cc.repositories import RetrievalError
from monkey_island.cc.services import IAgentPluginService
from monkey_island.cc.services.agent_plugin_service.flask_resources.available_agent_plugins_index import (  # noqa: E501
    AvailableAgentPluginsIndex,
)

SSH_EXPLOITER = [
    {
        "name": "SSH",
        "plugin_type": "Exploiter",
        "resource_path": "SSH-exploiter-v1.0.0.tar",
        "sha256": "862d4fd8c9d6c51926d34ac083f75c99d4fe4c3b3052de9e3d5995382a277a43",
        "description": "Attempts a brute-force attack against SSH using known "
        "credentials, including SSH keys.",
        "version": "1.0.0",
        "safe": True,
    }
]

EXPECTED_SERIALIZED_AGENT_PLUGIN_REPOSITORY_INDEX = {
    "timestamp": 1692629886.4792287,
    "compatible_infection_monkey_version": "development",
    "plugins": {
        "Credentials_Collector": {},
        "Exploiter": {
            "SSH": SSH_EXPLOITER,
        },
        "Fingerprinter": {},
        "Payload": {},
    },
}


@pytest.fixture
def agent_plugin_repository_index() -> AgentPluginRepositoryIndex:
    return AgentPluginRepositoryIndex(**EXPECTED_SERIALIZED_AGENT_PLUGIN_REPOSITORY_INDEX)


@pytest.fixture
def agent_plugin_service() -> IAgentPluginService:
    return MagicMock(spec=IAgentPluginService)


@pytest.fixture
def flask_client(build_flask_client, agent_plugin_service: IAgentPluginService):
    container = StubDIContainer()
    container.register_instance(IAgentPluginService, agent_plugin_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_available_agent_plugins_index(
    agent_plugin_service: IAgentPluginService,
    flask_client,
    agent_plugin_repository_index: AgentPluginRepositoryIndex,
):
    agent_plugin_service.get_available_plugins = MagicMock(
        return_value=agent_plugin_repository_index
    )
    resp = flask_client.get(
        get_url_for_resource(AvailableAgentPluginsIndex),
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json == EXPECTED_SERIALIZED_AGENT_PLUGIN_REPOSITORY_INDEX


@pytest.mark.parametrize("error", [RetrievalError, ValueError, Exception])
def test_available_agent_plugins_index__internal_server_error(
    agent_plugin_service: IAgentPluginService, flask_client, error
):
    agent_plugin_service.get_available_plugins = MagicMock(side_effect=error)
    resp = flask_client.get(
        get_url_for_resource(AvailableAgentPluginsIndex),
        follow_redirects=True,
    )

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.parametrize("force_refresh", ["bla", 1, None, "1"])
def test_available_agent_plugins_index__wrong_parameter(flask_client, force_refresh):
    resp = flask_client.get(
        get_url_for_resource(AvailableAgentPluginsIndex) + f"?force_refresh={force_refresh}",
        follow_redirects=True,
    )
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("force_refresh, refresh_boolean_value", [("true", True), ("false", False)])
def test_available_agent_plugins_index__right_parameter(
    agent_plugin_service: IAgentPluginService,
    flask_client,
    force_refresh,
    refresh_boolean_value: bool,
):
    resp = flask_client.get(
        get_url_for_resource(AvailableAgentPluginsIndex) + f"?force_refresh={force_refresh}",
        follow_redirects=True,
    )
    assert resp.status_code == HTTPStatus.OK
    agent_plugin_service.get_available_plugins.assert_called_with(
        force_refresh=refresh_boolean_value
    )

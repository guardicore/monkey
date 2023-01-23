from http import HTTPStatus

import pytest
from tests.common import StubDIContainer
from tests.monkey_island import InMemoryAgentPluginRepository
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_NAME, FAKE_TYPE
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import (
    FAKE_AGENT_PLUGIN_1,
    FAKE_PLUGIN_CONFIG_SCHEMA_1,
)
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.repositories import IAgentPluginRepository, RetrievalError
from monkey_island.cc.resources import AgentPlugins

FAKE_PLUGIN_NAME = "plugin_abc"


@pytest.fixture
def agent_plugin_repository():
    return InMemoryAgentPluginRepository()


@pytest.fixture
def flask_client(build_flask_client, agent_plugin_repository):
    container = StubDIContainer()
    container.register_instance(IAgentPluginRepository, agent_plugin_repository)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_get_plugin(flask_client, agent_plugin_repository):
    agent_plugin_repository.save_plugin(FAKE_AGENT_PLUGIN_1)

    expected_response = {
        "config_schema": FAKE_PLUGIN_CONFIG_SCHEMA_1,
        "plugin_manifest": {
            "description": None,
            "link_to_documentation": "www.beefface.com",
            "name": FAKE_NAME,
            "plugin_type": FAKE_TYPE,
            "safe": False,
            "remediation_suggestion": None,
            "target_operating_systems": ["linux"],
            "title": "Remote Desktop Protocol exploiter",
        },
        "source_archive": "cmFuZG9tIGJ5dGVz",
        "supported_operating_systems": ["linux"],
    }

    resp = flask_client.get(
        get_url_for_resource(
            AgentPlugins,
            host_os="linux",
            plugin_type=FAKE_TYPE,
            name=FAKE_AGENT_PLUGIN_1.plugin_manifest.name,
        )
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json == expected_response


def test_get_plugins__not_found_if_name_does_not_exist(flask_client):
    resp = flask_client.get(
        get_url_for_resource(AgentPlugins, host_os="linux", plugin_type=FAKE_TYPE, name="name")
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "type_",
    ["DummyType", "ExploiteR"],
)
def test_get_plugins__not_found_if_type_is_invalid(flask_client, type_):
    resp = flask_client.get(
        get_url_for_resource(AgentPlugins, host_os="linux", plugin_type=type_, name=FAKE_NAME)
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND


def test_get_plugins__server_error(flask_client, agent_plugin_repository):
    def raise_retrieval_error(host_os, plugin_type, name):
        raise RetrievalError

    agent_plugin_repository.get_plugin = raise_retrieval_error

    resp = flask_client.get(
        get_url_for_resource(AgentPlugins, host_os="linux", plugin_type=FAKE_TYPE, name=FAKE_NAME)
    )

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.parametrize(
    "os_",
    ["macos", "darwin"],
)
def test_get_plugins__not_found_if_os_is_invalid(flask_client, os_):
    resp = flask_client.get(
        get_url_for_resource(AgentPlugins, host_os=os_, plugin_type=FAKE_TYPE, name=FAKE_NAME)
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND

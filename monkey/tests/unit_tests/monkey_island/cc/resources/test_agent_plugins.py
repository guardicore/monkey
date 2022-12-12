from http import HTTPStatus

import pytest
from tests.common import StubDIContainer
from tests.monkey_island import InMemoryAgentPluginRepository
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_TYPE
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import FAKE_AGENT_PLUGIN_1
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.repositories import IAgentPluginRepository
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
    agent_plugin_repository.save_plugin(FAKE_PLUGIN_NAME, FAKE_AGENT_PLUGIN_1)

    expected_response = {
        "config_schema": {"plugin_options": {"some_option": "some_value"}},
        "plugin_manifest": {
            "description": None,
            "link_to_documentation": "www.beefface.com",
            "name": "rdp_exploiter",
            "plugin_type": "Exploiter",
            "safe": False,
            "supported_operating_systems": ["linux"],
            "title": "Remote Desktop Protocol exploiter",
        },
        "source_archive": "cmFuZG9tIGJ5dGVz",
    }

    resp = flask_client.get(
        get_url_for_resource(AgentPlugins, type=FAKE_TYPE, name=FAKE_PLUGIN_NAME)
    )

    assert resp.status_code == HTTPStatus.OK
    assert resp.json == expected_response


@pytest.mark.parametrize(
    "type, name",
    [
        ("DummyType", FAKE_PLUGIN_NAME),
        ("ExploiteR", FAKE_PLUGIN_NAME),
        ("Exploiter", "XYZ"),
        ("Payload", ""),
        ("", ""),
    ],
)
def test_plugins_not_found(flask_client, type, name):
    resp = flask_client.get(get_url_for_resource(AgentPlugins, type=type, name=name))

    assert resp.status_code == HTTPStatus.NOT_FOUND

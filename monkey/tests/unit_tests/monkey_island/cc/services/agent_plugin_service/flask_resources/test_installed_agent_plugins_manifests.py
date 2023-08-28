from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.monkey_island import InMemoryAgentPluginRepository
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import (
    FAKE_NAME,
    FAKE_NAME2,
    FAKE_TYPE,
)
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import (
    FAKE_AGENT_PLUGIN_1,
    FAKE_AGENT_PLUGIN_2,
)
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from common import OperatingSystem
from monkey_island.cc.repositories import RetrievalError
from monkey_island.cc.services.agent_plugin_service import IAgentPluginService
from monkey_island.cc.services.agent_plugin_service.agent_plugin_service import AgentPluginService
from monkey_island.cc.services.agent_plugin_service.flask_resources import (
    InstalledAgentPluginsManifests,
)

FAKE_PLUGIN_NAME = "plugin_abc"


@pytest.fixture
def agent_plugin_repository():
    return InMemoryAgentPluginRepository()


@pytest.fixture
def agent_plugin_service(agent_plugin_repository):
    return AgentPluginService(agent_plugin_repository, MagicMock())


@pytest.fixture
def flask_client(build_flask_client, agent_plugin_service):
    container = StubDIContainer()
    container.register_instance(IAgentPluginService, agent_plugin_service)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_get_installed_plugins_manifests(flask_client, agent_plugin_repository):
    agent_plugin_repository.store_agent_plugin(OperatingSystem.LINUX, FAKE_AGENT_PLUGIN_1)
    agent_plugin_repository.store_agent_plugin(OperatingSystem.WINDOWS, FAKE_AGENT_PLUGIN_2)

    expected_response = {
        "Exploiter": {
            FAKE_NAME: {
                "description": None,
                "link_to_documentation": "http://www.beefface.com",
                "name": FAKE_NAME,
                "plugin_type": FAKE_TYPE,
                "version": "1.0.0",
                "safe": False,
                "remediation_suggestion": None,
                "supported_operating_systems": ["linux", "windows"],
                "target_operating_systems": ["linux"],
                "title": "Remote Desktop Protocol exploiter",
            },
            FAKE_NAME2: {
                "description": None,
                "link_to_documentation": "http://www.beefface.com",
                "name": FAKE_NAME2,
                "plugin_type": FAKE_TYPE,
                "version": "1.0.0",
                "safe": False,
                "remediation_suggestion": None,
                "supported_operating_systems": ["linux", "windows"],
                "target_operating_systems": ["linux"],
                "title": "Remote Desktop Protocol exploiter",
            },
        }
    }

    resp = flask_client.get(get_url_for_resource(InstalledAgentPluginsManifests))

    assert resp.status_code == HTTPStatus.OK
    assert resp.json == expected_response


def test_get_installed_plugins_manifests__empty(flask_client):
    resp = flask_client.get(get_url_for_resource(InstalledAgentPluginsManifests))

    assert resp.status_code == HTTPStatus.OK
    assert resp.json == {}


def test_get_installed_plugins_manifests__server_error(flask_client, agent_plugin_repository):
    def raise_retrieval_error():
        raise RetrievalError

    agent_plugin_repository.get_all_plugin_manifests = raise_retrieval_error

    resp = flask_client.get(get_url_for_resource(InstalledAgentPluginsManifests))

    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

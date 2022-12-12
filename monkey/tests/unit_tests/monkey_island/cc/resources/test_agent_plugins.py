from http import HTTPStatus

import pytest
from tests.common import StubDIContainer
from tests.monkey_island import InMemoryAgentPluginRepository
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.repositories import IAgentPluginRepository
from monkey_island.cc.resources import AgentPlugins


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()
    container.register_instance(IAgentPluginRepository, InMemoryAgentPluginRepository())

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_plugins_not_found(flask_client):
    resp = flask_client.get(get_url_for_resource(AgentPlugins, type="DummyType", name="DummyName"))

    assert resp.status_code == HTTPStatus.NOT_FOUND

import json

import pytest
from tests.common import StubDIContainer
from tests.common.example_agent_configuration import AGENT_CONFIGURATION
from tests.monkey_island import InMemoryAgentConfigurationRepository
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.repository import IAgentConfigurationRepository
from monkey_island.cc.resources.agent_configuration import AgentConfiguration


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()

    container.register(IAgentConfigurationRepository, InMemoryAgentConfigurationRepository)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_agent_configuration_endpoint(flask_client):
    agent_configuration_url = get_url_for_resource(AgentConfiguration)

    flask_client.post(
        agent_configuration_url, data=json.dumps(AGENT_CONFIGURATION), follow_redirects=True
    )
    resp = flask_client.get(agent_configuration_url)

    assert resp.status_code == 200
    assert json.loads(resp.data) == AGENT_CONFIGURATION


def test_agent_configuration_invalid_config(flask_client):
    agent_configuration_url = get_url_for_resource(AgentConfiguration)

    resp = flask_client.post(
        agent_configuration_url, data=json.dumps({"invalid_config": "invalid_stuff"})
    )

    assert resp.status_code == 400


def test_agent_configuration_invalid_json(flask_client):
    agent_configuration_url = get_url_for_resource(AgentConfiguration)

    resp = flask_client.post(agent_configuration_url, data="InvalidJson!")

    assert resp.status_code == 400

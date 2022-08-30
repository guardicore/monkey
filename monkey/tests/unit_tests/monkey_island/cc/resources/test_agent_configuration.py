import json

import pytest
from tests.common import StubDIContainer
from tests.common.example_agent_configuration import AGENT_CONFIGURATION
from tests.monkey_island import InMemoryAgentConfigurationRepository
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.repository import IAgentConfigurationRepository
from monkey_island.cc.resources import AgentConfiguration as AgentConfigurationResource

AGENT_CONFIGURATION_URL = get_url_for_resource(AgentConfigurationResource)


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()

    container.register(IAgentConfigurationRepository, InMemoryAgentConfigurationRepository)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_agent_configuration_endpoint(flask_client):
    resp = flask_client.put(
        AGENT_CONFIGURATION_URL,
        json=AgentConfiguration(**AGENT_CONFIGURATION).dict(),
        follow_redirects=True,
    )
    assert resp.status_code == 200
    resp = flask_client.get(AGENT_CONFIGURATION_URL)

    assert resp.status_code == 200

    assert AgentConfiguration(**json.loads(resp.data)) == AgentConfiguration(**AGENT_CONFIGURATION)


def test_agent_configuration_invalid_config(flask_client):
    resp = flask_client.put(AGENT_CONFIGURATION_URL, json={"invalid_config": "invalid_stuff"})

    assert resp.status_code == 400


def test_agent_configuration_invalid_json(flask_client):
    resp = flask_client.put(AGENT_CONFIGURATION_URL, data="InvalidJson!")

    assert resp.status_code == 400

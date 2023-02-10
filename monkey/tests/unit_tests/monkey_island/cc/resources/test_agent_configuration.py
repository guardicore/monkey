import json
from copy import deepcopy

import pytest
from tests.common import StubDIContainer
from tests.common.example_agent_configuration import AGENT_CONFIGURATION
from tests.monkey_island import InMemoryAgentConfigurationRepository, InMemoryAgentPluginRepository
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import FAKE_AGENT_PLUGIN_1
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.repositories import (
    AgentConfigurationValidationDecorator,
    IAgentConfigurationRepository,
)
from monkey_island.cc.repositories.utils import AgentConfigurationSchemaCompiler
from monkey_island.cc.resources import AgentConfiguration as AgentConfigurationResource

AGENT_CONFIGURATION_URL = get_url_for_resource(AgentConfigurationResource)


@pytest.fixture
def in_memory_agent_plugin_repository():
    return InMemoryAgentPluginRepository()


@pytest.fixture
def flask_client(build_flask_client, in_memory_agent_plugin_repository):
    container = StubDIContainer()

    agent_configuration_schema_compiler = AgentConfigurationSchemaCompiler(
        in_memory_agent_plugin_repository
    )
    agent_configuration_repository = AgentConfigurationValidationDecorator(
        InMemoryAgentConfigurationRepository(), agent_configuration_schema_compiler
    )

    container.register_instance(IAgentConfigurationRepository, agent_configuration_repository)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_agent_configuration_endpoint(flask_client):
    resp = flask_client.put(
        AGENT_CONFIGURATION_URL,
        json=AgentConfiguration(**AGENT_CONFIGURATION).dict(simplify=True),
        follow_redirects=True,
    )
    print(resp.data)
    assert resp.status_code == 200
    resp = flask_client.get(AGENT_CONFIGURATION_URL)

    assert resp.status_code == 200

    assert AgentConfiguration(**json.loads(resp.data)) == AgentConfiguration(**AGENT_CONFIGURATION)


def test_agent_configuration_endpoint__bogus_data(flask_client, in_memory_agent_plugin_repository):
    in_memory_agent_plugin_repository.save_plugin(FAKE_AGENT_PLUGIN_1)
    agent_configuration = deepcopy(AGENT_CONFIGURATION)

    agent_configuration["propagation"]["exploitation"]["exploiters"] = {
        "bogus_exploiter": {"bogus_field": "bogus_value"}
    }

    resp = flask_client.put(
        AGENT_CONFIGURATION_URL,
        json=AgentConfiguration(**agent_configuration).dict(simplify=True),
        follow_redirects=True,
    )
    assert resp.status_code == 400


def test_agent_configuration_endpoint__invalid_plugin_data(
    flask_client, in_memory_agent_plugin_repository
):
    in_memory_agent_plugin_repository.save_plugin(FAKE_AGENT_PLUGIN_1)
    agent_configuration = deepcopy(AGENT_CONFIGURATION)

    agent_configuration["propagation"]["exploitation"]["exploiters"] = {
        FAKE_AGENT_PLUGIN_1.plugin_manifest.name: {
            "exploitation_success_rate": -123,
            "propagation_success_rate": 321,
        }
    }

    resp = flask_client.put(
        AGENT_CONFIGURATION_URL,
        json=AgentConfiguration(**agent_configuration).dict(simplify=True),
        follow_redirects=True,
    )
    assert resp.status_code == 400


def test_agent_configuration_invalid_config(flask_client):
    resp = flask_client.put(AGENT_CONFIGURATION_URL, json={"invalid_config": "invalid_stuff"})

    assert resp.status_code == 400


def test_agent_configuration_invalid_json(flask_client):
    resp = flask_client.put(AGENT_CONFIGURATION_URL, data="InvalidJson!")

    assert resp.status_code == 400

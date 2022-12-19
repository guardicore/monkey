from copy import deepcopy
from typing import Any, Dict

import pytest
from tests.monkey_island import InMemoryAgentPluginRepository
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import (
    FAKE_AGENT_PLUGIN_1,
    FAKE_AGENT_PLUGIN_2,
)

from common.agent_configuration import AgentConfiguration, PluginConfiguration
from common.agent_plugins import AgentPlugin
from monkey_island.cc.repositories import IAgentPluginRepository
from monkey_island.cc.services import ConfigSchemaService


@pytest.fixture
def expected_config_schema() -> Dict[str, Any]:
    expected_schema = deepcopy(AgentConfiguration.schema())
    expected_schema["definitions"]["AgentPluginsConfiguration"] = {
        "exploiter": {
            "anyOf": [
                expected_plugin_schema(FAKE_AGENT_PLUGIN_1),
                expected_plugin_schema(FAKE_AGENT_PLUGIN_2),
            ]
        },
    }
    expected_exploitation = expected_schema["definitions"]["ExploitationConfiguration"]
    expected_brute_force = expected_exploitation["properties"]["brute_force"]
    expected_brute_force["items"] = {"$ref": "#/definitions/AgentPluginsConfiguration/exploiter"}

    return expected_schema


@pytest.fixture
def agent_plugin_repository() -> IAgentPluginRepository:
    return InMemoryAgentPluginRepository()


@pytest.fixture
def config_schema_service(
    agent_plugin_repository: IAgentPluginRepository,
) -> ConfigSchemaService:
    return ConfigSchemaService(agent_plugin_repository)


def expected_plugin_schema(plugin: AgentPlugin):
    schema = deepcopy(PluginConfiguration.schema())
    # Need to specify the name here, otherwise the options can be matched with
    # any plugin's configuration
    schema["properties"]["name"]["enum"] = [plugin.plugin_manifest.name]
    schema["properties"]["options"]["properties"] = plugin.config_schema

    return schema


def test_get_schema__returns_config_schema(config_schema_service):
    schema = config_schema_service.get_schema()
    assert schema == deepcopy(AgentConfiguration.schema())


def test_get_schema__adds_exploiter_plugins_to_schema(
    config_schema_service, agent_plugin_repository, expected_config_schema
):
    agent_plugin_repository.save_plugin("ssh_exploiter", FAKE_AGENT_PLUGIN_1)
    agent_plugin_repository.save_plugin("wmi_exploiter", FAKE_AGENT_PLUGIN_2)

    actual_config_schema = config_schema_service.get_schema()
    assert actual_config_schema == expected_config_schema

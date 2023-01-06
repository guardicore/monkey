from copy import deepcopy

import pytest
from tests.monkey_island import InMemoryAgentPluginRepository
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_NAME, FAKE_NAME2
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import (
    FAKE_AGENT_PLUGIN_1,
    FAKE_AGENT_PLUGIN_2,
)

from common.agent_configuration import PluginConfiguration
from common.agent_plugins import AgentPlugin
from monkey_island.cc.repositories import IAgentPluginRepository
from monkey_island.cc.repositories.utils import AgentConfigurationSchemaCompiler
from monkey_island.cc.repositories.utils.hard_coded_exploiters import HARD_CODED_EXPLOITER_PLUGINS
from monkey_island.cc.services import AgentConfigurationSchemaService


@pytest.fixture
def agent_plugin_repository() -> IAgentPluginRepository:
    return InMemoryAgentPluginRepository()


@pytest.fixture
def config_schema_service(
    agent_plugin_repository: IAgentPluginRepository,
) -> AgentConfigurationSchemaService:
    return AgentConfigurationSchemaService(
        AgentConfigurationSchemaCompiler(agent_plugin_repository)
    )


def expected_plugin_schema(plugin: AgentPlugin):
    schema = deepcopy(PluginConfiguration.schema())
    # Need to specify the name here, otherwise the options can be matched with
    # any plugin's configuration
    schema["properties"]["name"]["title"] = plugin.plugin_manifest.title
    schema["properties"]["options"]["properties"] = plugin.config_schema

    return schema


EXPECTED_PLUGIN_SCHEMA = {  # type: ignore[index]
    FAKE_NAME: FAKE_AGENT_PLUGIN_1.config_schema,
    FAKE_NAME2: FAKE_AGENT_PLUGIN_2.config_schema,
}
EXPECTED_PLUGIN_SCHEMA.update(HARD_CODED_EXPLOITER_PLUGINS)


def test_get_schema__adds_exploiter_plugins_to_schema(
    config_schema_service, agent_plugin_repository
):
    agent_plugin_repository.save_plugin(FAKE_AGENT_PLUGIN_1)
    agent_plugin_repository.save_plugin(FAKE_AGENT_PLUGIN_2)

    actual_config_schema = config_schema_service.get_schema()
    retrieved_exploiter_schema = actual_config_schema["definitions"]["ExploitationConfiguration"][
        "properties"
    ]["exploiters"]["properties"]
    assert retrieved_exploiter_schema == EXPECTED_PLUGIN_SCHEMA

from copy import deepcopy

import pytest
from tests.monkey_island import InMemoryAgentPluginRepository
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_NAME, FAKE_NAME2
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import (
    FAKE_AGENT_PLUGIN_1,
    FAKE_AGENT_PLUGIN_2,
)

from monkey_island.cc.repositories import IAgentPluginRepository
from monkey_island.cc.repositories.utils import AgentConfigurationSchemaCompiler
from monkey_island.cc.repositories.utils.hard_coded_exploiter_schemas import (
    HARD_CODED_EXPLOITER_SCHEMAS,
)
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


@pytest.fixture
def expected_exploiters_plugin_schema():
    expected_exploiters_plugin_schema = deepcopy(HARD_CODED_EXPLOITER_SCHEMAS)
    expected_exploiters_plugin_schema[FAKE_NAME] = FAKE_AGENT_PLUGIN_1.config_schema
    expected_exploiters_plugin_schema[FAKE_NAME2] = FAKE_AGENT_PLUGIN_2.config_schema

    return expected_exploiters_plugin_schema


def test_get_schema__adds_exploiter_plugins_to_schema(
    config_schema_service, agent_plugin_repository, expected_exploiters_plugin_schema
):
    agent_plugin_repository.save_plugin(FAKE_AGENT_PLUGIN_1)
    agent_plugin_repository.save_plugin(FAKE_AGENT_PLUGIN_2)

    actual_config_schema = config_schema_service.get_schema()

    assert (
        actual_config_schema["definitions"]["ExploitationConfiguration"]["properties"][
            "exploiters"
        ]["properties"]
        == expected_exploiters_plugin_schema
    )

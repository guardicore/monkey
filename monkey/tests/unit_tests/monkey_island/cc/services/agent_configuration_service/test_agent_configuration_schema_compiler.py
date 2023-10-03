import copy
from unittest.mock import MagicMock

import pytest
from tests.common.fake_manifests import FAKE_NAME, FAKE_NAME2
from tests.monkey_island import InMemoryAgentPluginRepository
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import (
    FAKE_AGENT_PLUGIN_1,
    FAKE_AGENT_PLUGIN_2,
)

from common import OperatingSystem
from monkey_island.cc.services.agent_configuration_service.agent_configuration_schema_compiler import (  # noqa: E501
    AgentConfigurationSchemaCompiler,
)
from monkey_island.cc.services.agent_plugin_service import IAgentPluginService
from monkey_island.cc.services.agent_plugin_service.agent_plugin_service import AgentPluginService


@pytest.fixture
def agent_plugin_repository() -> InMemoryAgentPluginRepository:
    return InMemoryAgentPluginRepository()


@pytest.fixture
def agent_plugin_service(
    agent_plugin_repository: InMemoryAgentPluginRepository,
) -> IAgentPluginService:
    return AgentPluginService(agent_plugin_repository, MagicMock())


@pytest.fixture
def config_schema_compiler(
    agent_plugin_service: IAgentPluginService,
) -> AgentConfigurationSchemaCompiler:
    return AgentConfigurationSchemaCompiler(agent_plugin_service)


def test_get_schema__adds_exploiter_plugins_to_schema(
    config_schema_compiler: AgentConfigurationSchemaCompiler, agent_plugin_repository
):
    agent_plugin_repository.store_agent_plugin(OperatingSystem.LINUX, FAKE_AGENT_PLUGIN_1)
    agent_plugin_repository.store_agent_plugin(OperatingSystem.LINUX, FAKE_AGENT_PLUGIN_2)
    expected_fake_schema1 = copy.deepcopy(FAKE_AGENT_PLUGIN_1.config_schema)
    expected_fake_schema1.update(FAKE_AGENT_PLUGIN_1.plugin_manifest.dict(simplify=True))

    expected_fake_schema2 = copy.deepcopy(FAKE_AGENT_PLUGIN_2.config_schema)
    expected_fake_schema2.update(FAKE_AGENT_PLUGIN_2.plugin_manifest.dict(simplify=True))

    actual_config_schema = config_schema_compiler.get_schema()

    assert (
        actual_config_schema["definitions"]["ExploitationConfiguration"]["properties"][
            "exploiters"
        ]["properties"][FAKE_NAME]
        == expected_fake_schema1
    )
    assert (
        actual_config_schema["definitions"]["ExploitationConfiguration"]["properties"][
            "exploiters"
        ]["properties"][FAKE_NAME2]
        == expected_fake_schema2
    )

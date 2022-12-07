import pytest
from tests.monkey_island import InMemoryAgentPluginRepository
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_MANIFEST_OBJECT

from common.agent_plugins import AgentPlugin, AgentPluginType
from monkey_island.cc.repositories import (
    AgentPluginRepositoryCachingDecorator,
    IAgentPluginRepository,
)

FAKE_PLUGIN_CONFIG_SCHEMA_1 = {"plugin_options": {"some_option": "some_value"}}

FAKE_PLUGIN_ARCHIVE_1 = b"random bytes"

FAKE_AGENT_PLUGIN_1 = AgentPlugin(
    plugin_manifest=FAKE_MANIFEST_OBJECT,
    config_schema=FAKE_PLUGIN_CONFIG_SCHEMA_1,
    source_archive=FAKE_PLUGIN_ARCHIVE_1,
)


FAKE_PLUGIN_CONFIG_SCHEMA_2 = {"plugin_options": {"other_option": "other_value"}}

FAKE_PLUGIN_ARCHIVE_2 = b"other random bytes"

FAKE_AGENT_PLUGIN_2 = AgentPlugin(
    plugin_manifest=FAKE_MANIFEST_OBJECT,
    config_schema=FAKE_PLUGIN_CONFIG_SCHEMA_2,
    source_archive=FAKE_PLUGIN_ARCHIVE_2,
)


@pytest.fixture
def in_memory_agent_plugin_repository() -> IAgentPluginRepository:
    return InMemoryAgentPluginRepository()


@pytest.fixture
def agent_plugin_repository(in_memory_agent_plugin_repository) -> IAgentPluginRepository:
    return AgentPluginRepositoryCachingDecorator(in_memory_agent_plugin_repository)


def test_get_cached_plugin(agent_plugin_repository, in_memory_agent_plugin_repository):
    in_memory_agent_plugin_repository.save_plugin("ssh_one", FAKE_AGENT_PLUGIN_1)
    request_1_plugin = agent_plugin_repository.get_plugin("ssh_one", AgentPluginType.EXPLOITER)

    in_memory_agent_plugin_repository.save_plugin("ssh_one", FAKE_AGENT_PLUGIN_2)
    request_2_plugin = agent_plugin_repository.get_plugin("ssh_one", AgentPluginType.EXPLOITER)

    assert request_2_plugin == request_1_plugin
    assert request_2_plugin != FAKE_AGENT_PLUGIN_2

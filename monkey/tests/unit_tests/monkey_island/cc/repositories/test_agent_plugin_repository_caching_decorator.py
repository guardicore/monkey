import pytest
from tests.monkey_island import InMemoryAgentPluginRepository
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import (
    FAKE_AGENT_PLUGIN_1,
    FAKE_AGENT_PLUGIN_2,
)

from common.agent_plugins import AgentPluginType
from monkey_island.cc.repositories import (
    AgentPluginRepositoryCachingDecorator,
    IAgentPluginRepository,
)


@pytest.fixture
def in_memory_agent_plugin_repository() -> IAgentPluginRepository:
    return InMemoryAgentPluginRepository()


@pytest.fixture
def agent_plugin_repository(in_memory_agent_plugin_repository) -> IAgentPluginRepository:
    return AgentPluginRepositoryCachingDecorator(in_memory_agent_plugin_repository)


def test_get_cached_plugin(agent_plugin_repository, in_memory_agent_plugin_repository):
    in_memory_agent_plugin_repository.save_plugin("ssh_one", FAKE_AGENT_PLUGIN_1)
    request_1_plugin = agent_plugin_repository.get_plugin(AgentPluginType.EXPLOITER, "ssh_one")

    in_memory_agent_plugin_repository.save_plugin("ssh_one", FAKE_AGENT_PLUGIN_2)
    request_2_plugin = agent_plugin_repository.get_plugin(AgentPluginType.EXPLOITER, "ssh_one")

    assert request_2_plugin == request_1_plugin
    assert request_2_plugin != FAKE_AGENT_PLUGIN_2


def test_get_cached_plugin_catalog(agent_plugin_repository, in_memory_agent_plugin_repository):
    in_memory_agent_plugin_repository.save_plugin("ssh_exploiter", FAKE_AGENT_PLUGIN_1)
    request_1_plugin_catalog = agent_plugin_repository.get_plugin_catalog()

    in_memory_agent_plugin_repository.save_plugin("wmi_exploiter", FAKE_AGENT_PLUGIN_2)
    request_2_plugin_catalog = agent_plugin_repository.get_plugin_catalog()

    assert request_2_plugin_catalog == request_1_plugin_catalog

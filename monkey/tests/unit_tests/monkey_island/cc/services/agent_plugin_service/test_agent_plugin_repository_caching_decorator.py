import pytest
from tests.monkey_island import InMemoryAgentPluginRepository
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import (
    FAKE_AGENT_PLUGIN_1,
    FAKE_AGENT_PLUGIN_2,
    FAKE_PLUGIN_ARCHIVE_2,
    FAKE_PLUGIN_CONFIG_SCHEMA_2,
)

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from monkey_island.cc.services.agent_plugin_service.agent_plugin_repository_caching_decorator import (  # noqa: E501
    AgentPluginRepositoryCachingDecorator,
)
from monkey_island.cc.services.agent_plugin_service.i_agent_plugin_repository import (
    IAgentPluginRepository,
)


@pytest.fixture
def in_memory_agent_plugin_repository() -> IAgentPluginRepository:
    return InMemoryAgentPluginRepository()


@pytest.fixture
def agent_plugin_repository(in_memory_agent_plugin_repository) -> IAgentPluginRepository:
    return AgentPluginRepositoryCachingDecorator(in_memory_agent_plugin_repository)


def test_get_cached_plugin(agent_plugin_repository, in_memory_agent_plugin_repository):
    common_name = FAKE_AGENT_PLUGIN_1.plugin_manifest.name

    manifest_params = FAKE_AGENT_PLUGIN_2.plugin_manifest.dict(simplify=True)
    manifest_params["name"] = common_name
    agent_plugin_with_same_name = AgentPlugin(
        plugin_manifest=AgentPluginManifest(**manifest_params),
        config_schema=FAKE_PLUGIN_CONFIG_SCHEMA_2,
        source_archive=FAKE_PLUGIN_ARCHIVE_2,
        supported_operating_systems=(OperatingSystem.LINUX,),
    )

    in_memory_agent_plugin_repository.store_agent_plugin(OperatingSystem.LINUX, FAKE_AGENT_PLUGIN_1)
    retrieved_plugin_1 = agent_plugin_repository.get_plugin(
        OperatingSystem.LINUX, AgentPluginType.EXPLOITER, common_name
    )

    in_memory_agent_plugin_repository.store_agent_plugin(
        OperatingSystem.LINUX, agent_plugin_with_same_name
    )
    retrieved_plugin_2 = agent_plugin_repository.get_plugin(
        OperatingSystem.LINUX, AgentPluginType.EXPLOITER, common_name
    )

    assert retrieved_plugin_1 == retrieved_plugin_2
    assert retrieved_plugin_2.config_schema != agent_plugin_with_same_name.config_schema


def test_get_cached_plugin_manifests(agent_plugin_repository, in_memory_agent_plugin_repository):
    in_memory_agent_plugin_repository.store_agent_plugin(OperatingSystem.LINUX, FAKE_AGENT_PLUGIN_1)
    request_1_plugin_manifests = agent_plugin_repository.get_all_plugin_manifests()

    in_memory_agent_plugin_repository.store_agent_plugin(OperatingSystem.LINUX, FAKE_AGENT_PLUGIN_2)
    request_2_plugin_manifests = agent_plugin_repository.get_all_plugin_manifests()

    assert request_2_plugin_manifests == request_1_plugin_manifests

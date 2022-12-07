import pytest

from common.agent_plugins import AgentPluginType
from monkey_island.cc.repositories import (
    FileAgentPluginRepository,
    LocalStorageFileRepository,
    RetrievalError,
)

from .test_plugin_archive_parser import EXPECTED_MANIFEST


@pytest.fixture
def agent_plugin_repository(plugin_data_dir) -> FileAgentPluginRepository:
    file_repository = LocalStorageFileRepository(plugin_data_dir)
    return FileAgentPluginRepository(file_repository)


def test_get_plugin(agent_plugin_repository):
    plugin = agent_plugin_repository.get_plugin(AgentPluginType.EXPLOITER, "test")

    assert plugin.plugin_manifest == EXPECTED_MANIFEST
    assert isinstance(plugin.config_schema, dict)
    assert len(plugin.source_archive) > 0


def test_get_plugin__RetrievalError_if_not_exist(agent_plugin_repository):
    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_plugin(AgentPluginType.EXPLOITER, "does_not_exist")


def test_get_plugin__RetrievalError_if_bad_plugin(agent_plugin_repository):
    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_plugin(AgentPluginType.EXPLOITER, "bad")

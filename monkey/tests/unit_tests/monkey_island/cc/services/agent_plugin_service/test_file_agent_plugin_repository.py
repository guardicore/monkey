from os.path import basename

import pytest
from tests.monkey_island import InMemoryFileRepository

from common import OperatingSystem
from common.agent_plugins import AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories import RetrievalError, UnknownRecordError
from monkey_island.cc.services.agent_plugin_service.file_agent_plugin_repository import (
    FileAgentPluginRepository,
)

EXPECTED_MANIFEST = AgentPluginManifest(
    name="test",
    plugin_type=AgentPluginType.EXPLOITER,
    supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
    target_operating_systems=(OperatingSystem.WINDOWS, OperatingSystem.LINUX),
    title="dummy-exploiter",
    version="1.0.0",
    description="A dummy exploiter",
    safe=True,
)


@pytest.fixture
def file_repository() -> InMemoryFileRepository:
    return InMemoryFileRepository()


@pytest.fixture
def agent_plugin_repository(file_repository: InMemoryFileRepository) -> FileAgentPluginRepository:
    return FileAgentPluginRepository(file_repository)


def test_get_plugin(plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository):
    with open(plugin_file, "rb") as file:
        file_repository.save_file(basename(plugin_file), file)
    plugin = agent_plugin_repository.get_plugin(
        OperatingSystem.WINDOWS, AgentPluginType.EXPLOITER, "test"
    )

    assert plugin.plugin_manifest == EXPECTED_MANIFEST
    assert isinstance(plugin.config_schema, dict)
    assert len(plugin.source_archive) == 168


def test_get_plugin__UnknownRecordError_if_not_exist(agent_plugin_repository):
    with pytest.raises(UnknownRecordError):
        agent_plugin_repository.get_plugin(
            OperatingSystem.WINDOWS, AgentPluginType.EXPLOITER, "does_not_exist"
        )


def test_get_plugin__RetrievalError_if_bad_plugin(
    bad_plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository
):
    with open(bad_plugin_file, "rb") as file:
        file_repository.save_file(basename(bad_plugin_file), file)
    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_plugin(
            OperatingSystem.WINDOWS, AgentPluginType.EXPLOITER, "bad"
        )


def test_get_plugin__RetrievalError_if_unsupported_os(
    plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository
):
    with open(plugin_file, "rb") as file:
        file_repository.save_file(basename(plugin_file), file)
    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_plugin("unrecognised OS", AgentPluginType.EXPLOITER, "test")


def test_get_all_plugin_manifests(
    plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository
):
    with open(plugin_file, "rb") as file:
        file_repository.save_file(basename(plugin_file), file)

    actual_plugin_manifests = agent_plugin_repository.get_all_plugin_manifests()

    assert actual_plugin_manifests == {AgentPluginType.EXPLOITER: {"test": EXPECTED_MANIFEST}}


def test_get_all_plugin_manifests__RetrievalError_if_bad_plugin_type(
    plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository
):
    with open(plugin_file, "rb") as file:
        file_repository.save_file("ssh-bogus.tar", file)

    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_all_plugin_manifests()

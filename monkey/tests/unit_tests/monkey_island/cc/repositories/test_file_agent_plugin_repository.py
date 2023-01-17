from os.path import basename

import pytest
from tests.monkey_island import InMemoryFileRepository

from common import OperatingSystem
from common.agent_plugins import AgentPluginType
from monkey_island.cc.repositories import (
    FileAgentPluginRepository,
    RetrievalError,
    UnknownRecordError,
)

from .test_plugin_archive_parser import EXPECTED_MANIFEST


@pytest.fixture
def file_repository() -> InMemoryFileRepository:
    return InMemoryFileRepository()


@pytest.fixture
def agent_plugin_repository(file_repository: InMemoryFileRepository) -> FileAgentPluginRepository:
    return FileAgentPluginRepository(file_repository)


def test_get_plugin(plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository):
    with open(plugin_file, "rb") as file:
        file_repository.save_file(basename(plugin_file), file)
    plugin = agent_plugin_repository.get_plugin(AgentPluginType.EXPLOITER, "test")

    assert plugin.plugin_manifest == EXPECTED_MANIFEST
    assert isinstance(plugin.config_schema, dict)
    assert len(plugin.source_archive) == 10240


def test_get_plugin__UnknownRecordError_if_not_exist(agent_plugin_repository):
    with pytest.raises(UnknownRecordError):
        agent_plugin_repository.get_plugin(AgentPluginType.EXPLOITER, "does_not_exist")


def test_get_plugin__RetrievalError_if_bad_plugin(
    bad_plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository
):
    with open(bad_plugin_file, "rb") as file:
        file_repository.save_file(basename(bad_plugin_file), file)
    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_plugin(AgentPluginType.EXPLOITER, "bad")


def test_get_plugin_for_os(
    plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository
):
    with open(plugin_file, "rb") as file:
        file_repository.save_file(basename(plugin_file), file)
    plugin = agent_plugin_repository.get_plugin_for_os(
        OperatingSystem.LINUX, AgentPluginType.EXPLOITER, "test"
    )

    assert plugin.plugin_manifest == EXPECTED_MANIFEST
    assert isinstance(plugin.config_schema, dict)
    assert len(plugin.source_archive) == 10240


def test_get_plugin_for_os__UnknownRecordError_if_not_exist(agent_plugin_repository):
    with pytest.raises(UnknownRecordError):
        agent_plugin_repository.get_plugin_for_os(
            OperatingSystem.LINUX, AgentPluginType.EXPLOITER, "does_not_exist"
        )


def test_get_plugin_for_os__RetrievalError_if_bad_plugin(
    bad_plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository
):
    with open(bad_plugin_file, "rb") as file:
        file_repository.save_file(basename(bad_plugin_file), file)
    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_plugin_for_os(
            OperatingSystem.LINUX, AgentPluginType.EXPLOITER, "bad"
        )


def test_get_plugin_catalog(
    plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository
):
    with open(plugin_file, "rb") as file:
        file_repository.save_file(basename(plugin_file), file)

    actual_plugin_catalog = agent_plugin_repository.get_plugin_catalog()

    assert actual_plugin_catalog == [
        (AgentPluginType.EXPLOITER, "test", (OperatingSystem.LINUX, OperatingSystem.WINDOWS)),
    ]


def test_get_plugin_catalog__RetrievalError_if_bad_plugin_type(
    plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository
):
    with open(plugin_file, "rb") as file:
        file_repository.save_file("ssh-bogus.tar", file)

    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_plugin_catalog()

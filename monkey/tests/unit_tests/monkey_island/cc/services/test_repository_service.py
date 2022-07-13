from dataclasses import replace
from unittest.mock import MagicMock

import pytest
from tests.monkey_island import InMemoryAgentConfigurationRepository

from common.configuration import AgentConfiguration
from monkey_island.cc.repository import IAgentConfigurationRepository, IFileRepository
from monkey_island.cc.services import RepositoryService

LINUX_FILENAME = "linux_pba_file.sh"
WINDOWS_FILENAME = "windows_pba_file.ps1"


@pytest.fixture
def agent_configuration(default_agent_configuration) -> AgentConfiguration:
    custom_pbas = replace(
        default_agent_configuration.custom_pbas,
        linux_filename=LINUX_FILENAME,
        windows_filename=WINDOWS_FILENAME,
    )
    return replace(default_agent_configuration, custom_pbas=custom_pbas)


@pytest.fixture
def agent_configuration_repository(agent_configuration) -> IAgentConfigurationRepository:
    agent_configuration_repository = InMemoryAgentConfigurationRepository()
    agent_configuration_repository.store_configuration(agent_configuration)

    return agent_configuration_repository


@pytest.fixture
def mock_file_repository():
    return MagicMock(spec=IFileRepository)


def test_reset_configuration__remove_pba_files(
    agent_configuration_repository, mock_file_repository
):
    repository_service = RepositoryService(agent_configuration_repository, mock_file_repository)

    repository_service.reset_agent_configuration()

    assert mock_file_repository.delete_file.called_with(LINUX_FILENAME)
    assert mock_file_repository.delete_file.called_with(WINDOWS_FILENAME)


def test_reset_configuration__agent_configuration_changed(
    agent_configuration_repository, agent_configuration, mock_file_repository
):
    mock_file_repository = MagicMock(spec=IFileRepository)
    repository_service = RepositoryService(agent_configuration_repository, mock_file_repository)

    repository_service.reset_agent_configuration()

    assert agent_configuration_repository.get_configuration() != agent_configuration

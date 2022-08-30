from unittest.mock import MagicMock

import pytest
from tests.monkey_island import InMemoryAgentConfigurationRepository

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.repository import (
    IAgentConfigurationRepository,
    ICredentialsRepository,
    IFileRepository,
)
from monkey_island.cc.services import RepositoryService

LINUX_FILENAME = "linux_pba_file.sh"
WINDOWS_FILENAME = "windows_pba_file.ps1"


@pytest.fixture
def agent_configuration(default_agent_configuration: AgentConfiguration) -> AgentConfiguration:
    custom_pbas = default_agent_configuration.custom_pbas.copy(
        update={"linux_filename": LINUX_FILENAME, "windows_filename": WINDOWS_FILENAME},
    )
    return default_agent_configuration.copy(update={"custom_pbas": custom_pbas})


@pytest.fixture
def agent_configuration_repository(
    agent_configuration: AgentConfiguration,
) -> IAgentConfigurationRepository:
    agent_configuration_repository = InMemoryAgentConfigurationRepository()
    agent_configuration_repository.store_configuration(agent_configuration)

    return agent_configuration_repository


@pytest.fixture
def mock_file_repository() -> IFileRepository:
    return MagicMock(spec=IFileRepository)


@pytest.fixture
def mock_credentials_repository() -> ICredentialsRepository:
    return MagicMock(spec=ICredentialsRepository)


@pytest.fixture
def repository_service(
    agent_configuration_repository, mock_file_repository, mock_credentials_repository
) -> RepositoryService:
    return RepositoryService(
        agent_configuration_repository, mock_file_repository, mock_credentials_repository
    )


def test_reset_configuration__remove_pba_files(repository_service, mock_file_repository):
    repository_service.reset_agent_configuration()

    assert mock_file_repository.delete_file.called_with(LINUX_FILENAME)
    assert mock_file_repository.delete_file.called_with(WINDOWS_FILENAME)


def test_reset_configuration__agent_configuration_changed(
    repository_service, agent_configuration_repository, agent_configuration
):
    repository_service.reset_agent_configuration()

    assert agent_configuration_repository.get_configuration() != agent_configuration


@pytest.mark.usefixtures("uses_database")
def test_clear_simulation_data(
    repository_service: RepositoryService,
    mock_credentials_repository: ICredentialsRepository,
    monkeypatch,
):
    monkeypatch.setattr("monkey_island.cc.services.repository_service.Database", MagicMock())
    repository_service.clear_simulation_data()

    mock_credentials_repository.remove_stolen_credentials.assert_called_once()

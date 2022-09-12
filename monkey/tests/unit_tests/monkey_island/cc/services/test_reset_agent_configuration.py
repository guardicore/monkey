from unittest.mock import MagicMock

import pytest
from tests.monkey_island import InMemoryAgentConfigurationRepository

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.repository import IAgentConfigurationRepository, IFileRepository
from monkey_island.cc.services import reset_agent_configuration

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
def callable_reset_agent_configuration(agent_configuration_repository, mock_file_repository):
    return reset_agent_configuration(agent_configuration_repository, mock_file_repository)


def test_reset_configuration__remove_pba_files(
    callable_reset_agent_configuration, mock_file_repository
):
    callable_reset_agent_configuration()

    assert mock_file_repository.delete_file.called_with(LINUX_FILENAME)
    assert mock_file_repository.delete_file.called_with(WINDOWS_FILENAME)


def test_reset_configuration__agent_configuration_changed(
    callable_reset_agent_configuration, agent_configuration_repository, agent_configuration
):
    callable_reset_agent_configuration()

    assert agent_configuration_repository.get_configuration() != agent_configuration

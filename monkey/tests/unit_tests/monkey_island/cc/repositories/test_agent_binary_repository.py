from unittest.mock import MagicMock

import pytest

from monkey_island.cc.repositories import AgentBinaryRepository, IFileRepository, RetrievalError

LINUX_AGENT_BINARY = b"linux_binary"
WINDOWS_AGENT_BINARY = b"windows_binary"


@pytest.fixture
def error_mock_file_repository():
    mock_file_repository = MagicMock(wraps=IFileRepository)
    mock_file_repository.open_file = MagicMock(side_effect=OSError)

    return mock_file_repository


@pytest.fixture
def agent_binary_repository(error_mock_file_repository):
    return AgentBinaryRepository(error_mock_file_repository)


def test_get_linux_binary_retrieval_error(agent_binary_repository):
    with pytest.raises(RetrievalError):
        agent_binary_repository.get_linux_binary()


def test_get_windows_binary_retrieval_error(agent_binary_repository):
    with pytest.raises(RetrievalError):
        agent_binary_repository.get_windows_binary()

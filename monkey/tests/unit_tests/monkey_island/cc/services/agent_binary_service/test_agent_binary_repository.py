import io
from unittest.mock import MagicMock

import pytest
from tests.monkey_island import InMemoryFileRepository

from common import OperatingSystem
from monkey_island.cc.repositories import IFileRepository, RetrievalError
from monkey_island.cc.services.agent_binary_service.agent_binary_repository import (
    LINUX_AGENT_FILE_NAME,
    WINDOWS_AGENT_FILE_NAME,
    AgentBinaryRepository,
)

LINUX_AGENT_BINARY = b"linux_binary"
WINDOWS_AGENT_BINARY = b"windows_binary"


@pytest.fixture
def agent_binary_repository():
    file_repository = InMemoryFileRepository()
    file_repository.save_file(LINUX_AGENT_FILE_NAME, io.BytesIO(LINUX_AGENT_BINARY))
    file_repository.save_file(WINDOWS_AGENT_FILE_NAME, io.BytesIO(WINDOWS_AGENT_BINARY))
    return AgentBinaryRepository(file_repository)


@pytest.mark.parametrize(
    "operating_system,expected_agent_binary",
    ([OperatingSystem.LINUX, LINUX_AGENT_BINARY], [OperatingSystem.WINDOWS, WINDOWS_AGENT_BINARY]),
)
def test_get_os_binary(
    agent_binary_repository, operating_system: OperatingSystem, expected_agent_binary: bytes
):
    assert (
        agent_binary_repository.get_agent_binary(operating_system).read() == expected_agent_binary
    )


@pytest.fixture
def error_mock_file_repository():
    mock_file_repository = MagicMock(wraps=IFileRepository)
    mock_file_repository.open_file = MagicMock(side_effect=OSError)

    return mock_file_repository


@pytest.fixture
def error_raising_agent_binary_repository(error_mock_file_repository):
    return AgentBinaryRepository(error_mock_file_repository)


def test_get_linux_binary_retrieval_error(error_raising_agent_binary_repository):
    with pytest.raises(RetrievalError):
        error_raising_agent_binary_repository.get_linux_binary()


def test_get_windows_binary_retrieval_error(error_raising_agent_binary_repository):
    with pytest.raises(RetrievalError):
        error_raising_agent_binary_repository.get_windows_binary()

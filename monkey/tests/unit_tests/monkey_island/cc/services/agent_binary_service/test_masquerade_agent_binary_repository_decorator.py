import io
from unittest.mock import MagicMock

import pytest

from monkey_island.cc.services.agent_binary_service.i_agent_binary_repository import (
    IAgentBinaryRepository,
)
from monkey_island.cc.services.agent_binary_service.masquerade_agent_binary_repository_decorator import (  # noqa: E501
    NULL_BYTES_LENGTH,
    MasqueradeAgentBinaryRepositoryDecorator,
)

LINUX_AGENT_BINARY = io.BytesIO(b"linux_binary")
WINDOWS_AGENT_BINARY = io.BytesIO(b"windows_binary")

MASQUE = b"m0nk3y"


@pytest.fixture
def mock_agent_binary_repository() -> IAgentBinaryRepository:
    mock_agent_binary_repository = MagicMock(wraps=IAgentBinaryRepository)

    mock_agent_binary_repository.get_linux_binary = MagicMock(return_value=LINUX_AGENT_BINARY)
    mock_agent_binary_repository.get_windows_binary = MagicMock(return_value=WINDOWS_AGENT_BINARY)

    return mock_agent_binary_repository


def test_masquerade_agent_binary_repository_decorator__linux(
    mock_agent_binary_repository: IAgentBinaryRepository,
):
    agent_binary_repository = MasqueradeAgentBinaryRepositoryDecorator(
        mock_agent_binary_repository, MASQUE
    )
    actual_linux_binary = agent_binary_repository.get_linux_binary()
    expected_linux_binary = LINUX_AGENT_BINARY
    expected_linux_binary.seek(0, io.SEEK_END)
    expected_linux_binary.write(b"\x00" * NULL_BYTES_LENGTH + MASQUE)
    assert actual_linux_binary == expected_linux_binary


def test_masquerade_agent_binary_repository_decorator__windows(
    mock_agent_binary_repository: IAgentBinaryRepository,
):
    agent_binary_repository = MasqueradeAgentBinaryRepositoryDecorator(
        mock_agent_binary_repository, MASQUE
    )
    actual_windows_binary = agent_binary_repository.get_windows_binary()

    expected_windows_binary = WINDOWS_AGENT_BINARY
    expected_windows_binary.seek(0, io.SEEK_END)
    expected_windows_binary.write(b"\x00" * NULL_BYTES_LENGTH + MASQUE)
    assert actual_windows_binary == expected_windows_binary


def test_masquerade_agent_binary_repository_decorator__cached_linux(
    mock_agent_binary_repository: IAgentBinaryRepository,
):
    agent_binary_repository = MasqueradeAgentBinaryRepositoryDecorator(
        mock_agent_binary_repository, MASQUE
    )
    actual_linux_binary = agent_binary_repository.get_linux_binary()
    mock_agent_binary_repository.get_linux_binary = MagicMock(return_value=b"not_linux_binary")
    cached_linux_binary = agent_binary_repository.get_linux_binary()

    assert actual_linux_binary == cached_linux_binary


def test_masquerade_agent_binary_repository_decorator__cached_windows(
    mock_agent_binary_repository: IAgentBinaryRepository,
):
    agent_binary_repository = MasqueradeAgentBinaryRepositoryDecorator(
        mock_agent_binary_repository, MASQUE
    )
    actual_windows_binary = agent_binary_repository.get_windows_binary()
    mock_agent_binary_repository.get_windows_binary = MagicMock(return_value=b"not_windows_binary")
    cached_windows_binary = agent_binary_repository.get_windows_binary()

    assert actual_windows_binary == cached_windows_binary

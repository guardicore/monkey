import io

import pytest
from tests.monkey_island import InMemoryAgentBinaryRepository

from common import OperatingSystem
from monkey_island.cc.services.agent_binary_service.i_agent_binary_repository import (
    IAgentBinaryRepository,
)
from monkey_island.cc.services.agent_binary_service.masquerade_agent_binary_repository_decorator import (  # noqa: E501
    MasqueradeAgentBinaryRepositoryDecorator,
)

NULL_BYTES_LENGTH = 8
MASQUE = b"m0nk3y"

LINUX_AGENT_BINARY_BYTES = b"linux_binary"
LINUX_AGENT_BINARY = io.BytesIO(LINUX_AGENT_BINARY_BYTES)
MASQUED_LINUX_AGENT_BINARY = io.BytesIO(
    LINUX_AGENT_BINARY_BYTES + b"\x00" * NULL_BYTES_LENGTH + MASQUE
)

WINDOWS_AGENT_BINARY_BYTES = b"windows_binary"
WINDOWS_AGENT_BINARY = io.BytesIO(WINDOWS_AGENT_BINARY_BYTES)
MASQUED_WINDOWS_AGENT_BINARY = io.BytesIO(
    WINDOWS_AGENT_BINARY_BYTES + b"\x00" * NULL_BYTES_LENGTH + MASQUE
)


@pytest.fixture
def in_memory_agent_binary_repository() -> InMemoryAgentBinaryRepository:
    return InMemoryAgentBinaryRepository()


@pytest.fixture
def mock_masquerade_agent_binary_repository(
    in_memory_agent_binary_repository: IAgentBinaryRepository,
) -> MasqueradeAgentBinaryRepositoryDecorator:
    return MasqueradeAgentBinaryRepositoryDecorator(
        in_memory_agent_binary_repository, MASQUE, NULL_BYTES_LENGTH
    )


@pytest.mark.parametrize(
    "operating_system,expected_agent_binary",
    (
        (OperatingSystem.LINUX, MASQUED_LINUX_AGENT_BINARY),
        (OperatingSystem.WINDOWS, MASQUED_WINDOWS_AGENT_BINARY),
    ),
)
def test_get_agent_binary(
    mock_masquerade_agent_binary_repository: MasqueradeAgentBinaryRepositoryDecorator,
    operating_system: OperatingSystem,
    expected_agent_binary: io.BytesIO,
):
    actual_linux_binary = mock_masquerade_agent_binary_repository.get_agent_binary(operating_system)

    assert actual_linux_binary.getvalue() == expected_agent_binary.getvalue()  # type: ignore[attr-defined] # noqa: E501


@pytest.mark.parametrize(
    "operating_system",
    (OperatingSystem.LINUX, OperatingSystem.WINDOWS),
)
def test_get_agent_binary__cached(
    in_memory_agent_binary_repository: InMemoryAgentBinaryRepository,
    mock_masquerade_agent_binary_repository: MasqueradeAgentBinaryRepositoryDecorator,
    operating_system: OperatingSystem,
):
    actual_linux_binary = mock_masquerade_agent_binary_repository.get_agent_binary(operating_system)
    in_memory_agent_binary_repository.agent_binaries[operating_system] = b"new_binary"
    cached_linux_binary = mock_masquerade_agent_binary_repository.get_agent_binary(operating_system)

    assert actual_linux_binary == cached_linux_binary

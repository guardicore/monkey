import io

import pytest
from monkeytypes import OperatingSystem
from tests.monkey_island import InMemoryAgentBinaryRepository
from tests.monkey_island.in_memory_masquerade_repository import InMemoryMasqueradeRepository

from monkey_island.cc.services.agent_binary_service.i_agent_binary_repository import (
    IAgentBinaryRepository,
)
from monkey_island.cc.services.agent_binary_service.i_masquerade_repository import (
    IMasqueradeRepository,
)
from monkey_island.cc.services.agent_binary_service.masquerade_agent_binary_repository_decorator import (  # noqa: E501
    MasqueradeAgentBinaryRepositoryDecorator,
)

NULL_BYTES_LENGTH = 8
LINUX_MASQUE = b"m0nk3y"
WINDOWS_MASQUE = b"m0nk3y"

LINUX_AGENT_BINARY_BYTES = b"linux_binary"
LINUX_AGENT_BINARY = io.BytesIO(LINUX_AGENT_BINARY_BYTES)
MASQUED_LINUX_AGENT_BINARY = io.BytesIO(
    LINUX_AGENT_BINARY_BYTES + b"\x00" * NULL_BYTES_LENGTH + LINUX_MASQUE
)

WINDOWS_AGENT_BINARY_BYTES = b"windows_binary"
WINDOWS_AGENT_BINARY = io.BytesIO(WINDOWS_AGENT_BINARY_BYTES)
MASQUED_WINDOWS_AGENT_BINARY = io.BytesIO(
    WINDOWS_AGENT_BINARY_BYTES + b"\x00" * NULL_BYTES_LENGTH + WINDOWS_MASQUE
)


@pytest.fixture
def in_memory_agent_binary_repository() -> InMemoryAgentBinaryRepository:
    return InMemoryAgentBinaryRepository()


@pytest.fixture
def in_memory_masquerade_repository() -> IMasqueradeRepository:
    return InMemoryMasqueradeRepository()


@pytest.fixture
def mock_masquerade_agent_binary_repository(
    in_memory_agent_binary_repository: IAgentBinaryRepository,
    in_memory_masquerade_repository: IMasqueradeRepository,
) -> MasqueradeAgentBinaryRepositoryDecorator:
    in_memory_masquerade_repository.set_masque(OperatingSystem.LINUX, LINUX_MASQUE)
    in_memory_masquerade_repository.set_masque(OperatingSystem.WINDOWS, WINDOWS_MASQUE)

    return MasqueradeAgentBinaryRepositoryDecorator(
        in_memory_agent_binary_repository, in_memory_masquerade_repository, NULL_BYTES_LENGTH
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
    actual_binary = mock_masquerade_agent_binary_repository.get_agent_binary(operating_system)

    assert actual_binary.read() == expected_agent_binary.getvalue()


def test_one_unset_masque(
    in_memory_agent_binary_repository: IAgentBinaryRepository,
    in_memory_masquerade_repository: IMasqueradeRepository,
):
    in_memory_masquerade_repository.set_masque(OperatingSystem.LINUX, LINUX_MASQUE)

    masquerade_agent_binary_repository = MasqueradeAgentBinaryRepositoryDecorator(
        in_memory_agent_binary_repository, in_memory_masquerade_repository, NULL_BYTES_LENGTH
    )

    actual_linux_binary = masquerade_agent_binary_repository.get_agent_binary(OperatingSystem.LINUX)
    actual_windows_binary = masquerade_agent_binary_repository.get_agent_binary(
        OperatingSystem.WINDOWS
    )

    assert actual_linux_binary.read() == MASQUED_LINUX_AGENT_BINARY.getvalue()
    assert actual_windows_binary.read() == WINDOWS_AGENT_BINARY.getvalue()

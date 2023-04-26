import io
from typing import Mapping

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
LINUX_MASQUE = b"m0nk3y"
WINDOWS_MASQUE = b"m0nk3y"
MASQUES = {OperatingSystem.LINUX: LINUX_MASQUE, OperatingSystem.WINDOWS: WINDOWS_MASQUE}

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
def mock_masquerade_agent_binary_repository(
    in_memory_agent_binary_repository: IAgentBinaryRepository,
) -> MasqueradeAgentBinaryRepositoryDecorator:
    return MasqueradeAgentBinaryRepositoryDecorator(
        in_memory_agent_binary_repository, MASQUES, NULL_BYTES_LENGTH
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


@pytest.mark.parametrize(
    "operating_system",
    (OperatingSystem.LINUX, OperatingSystem.WINDOWS),
)
def test_get_agent_binary__cached(
    in_memory_agent_binary_repository: InMemoryAgentBinaryRepository,
    mock_masquerade_agent_binary_repository: MasqueradeAgentBinaryRepositoryDecorator,
    operating_system: OperatingSystem,
):
    actual_binary = mock_masquerade_agent_binary_repository.get_agent_binary(operating_system)
    in_memory_agent_binary_repository.agent_binaries[operating_system] = b"new_binary"
    cached_binary = mock_masquerade_agent_binary_repository.get_agent_binary(operating_system)

    assert actual_binary.read() == cached_binary.read()


def test_get_agent_binary__cached_multiple_calls(
    in_memory_agent_binary_repository: InMemoryAgentBinaryRepository,
    mock_masquerade_agent_binary_repository: MasqueradeAgentBinaryRepositoryDecorator,
):
    operating_system = OperatingSystem.WINDOWS

    cached_binary_1 = mock_masquerade_agent_binary_repository.get_agent_binary(operating_system)
    in_memory_agent_binary_repository.agent_binaries[operating_system] = b"new_binary"
    cached_binary_2 = mock_masquerade_agent_binary_repository.get_agent_binary(operating_system)
    cached_binary_3 = mock_masquerade_agent_binary_repository.get_agent_binary(operating_system)

    # Writing the assertion this way verifies that returned files have had their positions reset to
    # the beginning (i.e. seek(0)).
    assert cached_binary_1.read() == MASQUED_WINDOWS_AGENT_BINARY.getvalue()
    assert cached_binary_2.read() == MASQUED_WINDOWS_AGENT_BINARY.getvalue()
    assert cached_binary_3.read() == MASQUED_WINDOWS_AGENT_BINARY.getvalue()


@pytest.mark.parametrize(
    "masques",
    (
        {OperatingSystem.LINUX: LINUX_MASQUE},
        {OperatingSystem.LINUX: LINUX_MASQUE, OperatingSystem.WINDOWS: None},
    ),
)
def test_one_unset_masque(
    in_memory_agent_binary_repository: IAgentBinaryRepository,
    masques: Mapping[OperatingSystem, bytes],
):
    masquerade_agent_binary_repository = MasqueradeAgentBinaryRepositoryDecorator(
        in_memory_agent_binary_repository, masques, NULL_BYTES_LENGTH
    )

    actual_linux_binary = masquerade_agent_binary_repository.get_agent_binary(OperatingSystem.LINUX)
    actual_windows_binary = masquerade_agent_binary_repository.get_agent_binary(
        OperatingSystem.WINDOWS
    )

    assert actual_linux_binary.read() == MASQUED_LINUX_AGENT_BINARY.getvalue()
    assert actual_windows_binary.read() == WINDOWS_AGENT_BINARY.getvalue()

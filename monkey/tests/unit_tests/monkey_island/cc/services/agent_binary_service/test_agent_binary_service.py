import pytest
from tests.monkey_island.in_memory_agent_binary_repository import (
    LINUX_AGENT_BINARY,
    WINDOWS_AGENT_BINARY,
    InMemoryAgentBinaryRepository,
)

from common import OperatingSystem
from monkey_island.cc.services import IAgentBinaryService
from monkey_island.cc.services.agent_binary_service.agent_binary_service import AgentBinaryService

BINARIES = {
    OperatingSystem.LINUX: LINUX_AGENT_BINARY,
    OperatingSystem.WINDOWS: WINDOWS_AGENT_BINARY,
}
MASQUES = {
    OperatingSystem.LINUX: b"linux-masque\xBE\xEF\x00\xFA\xCE",
    OperatingSystem.WINDOWS: b"windows-masque\x0F\xF1\xCE\x00\xBA\xBB\x1E",
}


@pytest.fixture
def agent_binary_service() -> IAgentBinaryService:
    return AgentBinaryService(InMemoryAgentBinaryRepository())


@pytest.mark.parametrize("operating_system", [OperatingSystem.LINUX, OperatingSystem.WINDOWS])
def test_get_masque__empty(
    agent_binary_service: IAgentBinaryService, operating_system: OperatingSystem
):
    assert agent_binary_service.get_masque(operating_system) is None


@pytest.mark.parametrize(
    "operating_system",
    [OperatingSystem.LINUX, OperatingSystem.WINDOWS],
)
def test_set_masque(agent_binary_service: IAgentBinaryService, operating_system: OperatingSystem):
    masque = MASQUES[operating_system]
    agent_binary_service.set_masque(operating_system, masque)

    assert agent_binary_service.get_masque(operating_system) == masque


@pytest.mark.parametrize(
    "operating_system",
    [OperatingSystem.LINUX, OperatingSystem.WINDOWS],
)
def test_unmasqued_agent_returned__masque_already_none(
    agent_binary_service: IAgentBinaryService, operating_system: OperatingSystem
):
    expected_agent_binary = BINARIES[operating_system]

    agent_binary_service.set_masque(operating_system, None)
    agent_binary = agent_binary_service.get_agent_binary(operating_system).read()

    assert agent_binary == expected_agent_binary


@pytest.mark.parametrize(
    "operating_system",
    [OperatingSystem.LINUX, OperatingSystem.WINDOWS],
)
def test_unmasqued_agent_returned__masque_already_set(
    agent_binary_service: IAgentBinaryService, operating_system: OperatingSystem
):
    expected_agent_binary = BINARIES[operating_system]
    agent_binary_service.set_masque(operating_system, b"some-masque")

    agent_binary_service.set_masque(operating_system, None)
    agent_binary = agent_binary_service.get_agent_binary(operating_system).read()

    assert agent_binary == expected_agent_binary


@pytest.mark.parametrize(
    "operating_system",
    [OperatingSystem.LINUX, OperatingSystem.WINDOWS],
)
def test_masqued_agent_returned(
    agent_binary_service: IAgentBinaryService, operating_system: OperatingSystem
):
    expected_agent_binary = BINARIES[operating_system]
    masque = MASQUES[operating_system]

    agent_binary_service.set_masque(operating_system, masque)
    agent_binary = agent_binary_service.get_agent_binary(operating_system).read()

    assert agent_binary.startswith(expected_agent_binary)
    assert agent_binary.endswith(masque)


@pytest.mark.parametrize(
    "operating_system",
    [OperatingSystem.LINUX, OperatingSystem.WINDOWS],
)
def test_masqued_agent_returned__replace_existing_masque(
    agent_binary_service: IAgentBinaryService, operating_system: OperatingSystem
):
    expected_agent_binary = BINARIES[operating_system]
    masque = MASQUES[operating_system]
    agent_binary_service.set_masque(operating_system, b"old-masque")

    agent_binary_service.set_masque(operating_system, masque)
    agent_binary = agent_binary_service.get_agent_binary(operating_system).read()

    assert agent_binary.startswith(expected_agent_binary)
    assert agent_binary.endswith(masque)

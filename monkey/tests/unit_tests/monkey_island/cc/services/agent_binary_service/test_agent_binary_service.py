from unittest.mock import MagicMock

import pytest

from common import OperatingSystem
from monkey_island.cc.services import IAgentBinaryService
from monkey_island.cc.services.agent_binary_service.agent_binary_service import AgentBinaryService
from monkey_island.cc.services.agent_binary_service.i_agent_binary_repository import (
    IAgentBinaryRepository,
)

LINUX_MASQUE = b"linux_masque"
WINDOWS_MASQUE = b"windows_masque"


@pytest.fixture
def mock_agent_binary_repository() -> IAgentBinaryRepository:
    return MagicMock(spec=IAgentBinaryRepository)


@pytest.fixture
def agent_binary_service(mock_agent_binary_repository) -> IAgentBinaryService:
    return AgentBinaryService(mock_agent_binary_repository)


@pytest.mark.parametrize("operating_system", [OperatingSystem.LINUX, OperatingSystem.WINDOWS])
def test_get_masque__empty(
    agent_binary_service: IAgentBinaryService, operating_system: OperatingSystem
):
    assert agent_binary_service.get_masque(operating_system) is None


@pytest.mark.parametrize(
    "masque, operating_system",
    [(LINUX_MASQUE, OperatingSystem.LINUX), (WINDOWS_MASQUE, OperatingSystem.WINDOWS)],
)
def test_set_masque(
    agent_binary_service: IAgentBinaryService, masque: bytes, operating_system: OperatingSystem
):
    agent_binary_service.set_masque(operating_system, masque)

    assert agent_binary_service.get_masque(operating_system) == masque

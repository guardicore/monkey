from unittest.mock import MagicMock

from common import OperatingSystem
from monkey_island.cc.models import IslandMode
from monkey_island.cc.services import IAgentBinaryService
from monkey_island.cc.services.agent_binary_service.event_handlers import (
    reset_masque_on_island_mode_change,
)


def test_reset_masque_on_island_mode_change():
    mock_agent_binary_service = MagicMock(spec=IAgentBinaryService)
    event_handler = reset_masque_on_island_mode_change(mock_agent_binary_service)

    event_handler(IslandMode.ADVANCED)

    for operating_system in OperatingSystem:
        mock_agent_binary_service.set_masque.assert_any_call(operating_system, None)

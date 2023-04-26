from common import OperatingSystem
from monkey_island.cc.models import IslandMode

from . import IAgentBinaryService


class reset_masque_on_island_mode_change:
    """
    Callable class that sets the default Agent configuration as per the Island's mode
    """

    def __init__(
        self,
        agent_binary_service: IAgentBinaryService,
    ):
        self._agent_binary_service = agent_binary_service

    def __call__(self, mode: IslandMode):
        for operating_system in OperatingSystem:
            self._agent_binary_service.set_masque(operating_system, None)

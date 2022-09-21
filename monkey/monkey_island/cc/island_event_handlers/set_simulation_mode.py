from typing import Any

from monkey_island.cc.repository import ISimulationRepository


class set_simulation_mode:
    """
    Callable class that sets the Island's mode
    """

    def __init__(
        self,
        simulation_repository: ISimulationRepository,
    ):
        self._simulation_repository = simulation_repository

    def __call__(self, event: Any = None):
        mode = event
        self._simulation_repository.set_mode(mode)

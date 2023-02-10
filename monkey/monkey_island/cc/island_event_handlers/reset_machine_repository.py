from monkey_island.cc.repositories import IMachineRepository, initialize_machine_repository


class reset_machine_repository:
    """
    Callable class that handles reset and reinitialization of IMachineRepository
    """

    def __init__(self, machine_repository: IMachineRepository):
        self._machine_repository = machine_repository

    def __call__(self):
        self._machine_repository.reset()
        initialize_machine_repository(self._machine_repository)

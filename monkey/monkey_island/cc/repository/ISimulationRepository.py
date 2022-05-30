from abc import ABC


class ISimulationRepository(ABC):
    # TODO define simulation object. It should contain metadata about simulation,
    # like start, end times, mode and last forced stop of all monkeys
    def save_simulation(self, simulation: Simulation):  # noqa: F821
        pass

    def get_simulation(self):
        pass

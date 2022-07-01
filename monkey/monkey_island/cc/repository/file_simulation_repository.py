import dataclasses
import io

from monkey_island.cc import repository
from monkey_island.cc.models import Simulation, SimulationSchema
from monkey_island.cc.repository import IFileRepository, ISimulationRepository, RetrievalError
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum

SIMULATION_STATE_FILE_NAME = "simulation_state.json"


class FileSimulationRepository(ISimulationRepository):
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository
        self._simulation_schema = SimulationSchema()

    def save_simulation(self, simulation: Simulation):
        simulation_json = self._simulation_schema.dumps(simulation)

        self._file_repository.save_file(
            SIMULATION_STATE_FILE_NAME, io.BytesIO(simulation_json.encode())
        )

    def get_simulation(self) -> Simulation:
        try:
            with self._file_repository.open_file(SIMULATION_STATE_FILE_NAME) as f:
                simulation_json = f.read().decode()

            return self._simulation_schema.loads(simulation_json)
        except repository.FileNotFoundError:
            return Simulation()
        except Exception as err:
            raise RetrievalError(f"Error retrieving the simulation state: {err}")

    def get_mode(self) -> IslandModeEnum:
        return self.get_simulation().mode

    def set_mode(self, mode: IslandModeEnum):
        old_simulation = self.get_simulation()
        new_simulation = dataclasses.replace(old_simulation, mode=mode)
        self.save_simulation(new_simulation)

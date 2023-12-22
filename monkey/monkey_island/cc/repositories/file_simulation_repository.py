import io

from monkey_island.cc import repositories
from monkey_island.cc.models import Simulation
from monkey_island.cc.repositories import IFileRepository, ISimulationRepository, RetrievalError

SIMULATION_STATE_FILE_NAME = "simulation_state.json"


class FileSimulationRepository(ISimulationRepository):
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository

    def get_simulation(self) -> Simulation:
        try:
            with self._file_repository.open_file(SIMULATION_STATE_FILE_NAME) as f:
                simulation_json = f.read().decode()

            return Simulation.model_validate_json(simulation_json)
        except repositories.FileNotFoundError:
            return Simulation()
        except Exception as err:
            raise RetrievalError(f"Error retrieving the simulation state: {err}")

    def save_simulation(self, simulation: Simulation):
        simulation_json = simulation.to_json()

        self._file_repository.save_file(
            SIMULATION_STATE_FILE_NAME, io.BytesIO(simulation_json.encode())
        )

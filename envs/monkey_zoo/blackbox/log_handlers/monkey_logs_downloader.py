import logging
from pathlib import Path
from typing import Mapping, Sequence

from common.types import MachineID
from monkey_island.cc.models import Agent, Machine

LOGGER = logging.getLogger(__name__)


class MonkeyLogsDownloader(object):
    def __init__(self, island_client, log_dir_path):
        self.island_client = island_client
        self.log_dir_path = Path(log_dir_path)
        self.monkey_log_paths: Sequence[Path] = []

    def download_monkey_logs(self):
        try:
            LOGGER.info("Downloading each monkey log.")

            agents = self.island_client.get_agents()
            machines = self.island_client.get_machines()

            for agent in agents:
                log_file_path = self._get_log_file_path(agent, machines)
                log_contents = self.island_client.get_agent_log(agent.id)

                MonkeyLogsDownloader._write_log_to_file(log_file_path, log_contents)

                self.monkey_log_paths.append(log_file_path)
        except Exception as err:
            LOGGER.exception(err)

    def _get_log_file_path(self, agent: Agent, machines: Mapping[MachineID, Machine]) -> Path:
        try:
            machine_ip = machines[agent.machine_id].network_interfaces[0].ip
        except IndexError:
            machine_ip = "UNKNOWN"

        start_time = agent.start_time.strftime("%Y-%m-%d-%H-%M-%S")

        return self.log_dir_path / f"agent-{start_time}-{machine_ip}.log"

    @staticmethod
    def _write_log_to_file(log_file_path: Path, log_contents: str):
        LOGGER.debug(f"Writing {len(log_contents)} bytes to {log_file_path}")

        with open(log_file_path, "w") as f:
            f.write(log_contents)

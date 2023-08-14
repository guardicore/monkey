import logging
from datetime import datetime
from pathlib import Path
from threading import Thread
from typing import List, Mapping

from common.types import MachineID
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.log_handlers.island_log_parser import IslandLogParser
from envs.monkey_zoo.blackbox.utils import bb_singleton
from monkey_island.cc.models import Agent, Machine

logger = logging.getLogger(__name__)


class MonkeyLogsDownloader(object):
    def __init__(self, island_client: MonkeyIslandClient, log_dir_path: str):
        self.island_client = island_client
        self.log_dir_path = Path(log_dir_path)
        self.monkey_log_paths: List[Path] = []

    def download_monkey_logs(self):
        try:
            logger.info("Downloading each monkey log.")

            agents = self.island_client.get_agents()
            machines = self.island_client.get_machines()

            download_threads: List[Thread] = []

            # TODO: Does downloading logs concurrently still improve performance after resolving
            #       https://github.com/guardicore/monkey/issues/2383?
            for agent in agents:
                t = Thread(target=self._download_agent_log, args=(agent, machines), daemon=True)
                t.start()
                download_threads.append(t)

            for thread in download_threads:
                thread.join()

            self._download_island_log()

        except Exception as err:
            logger.exception(err)

    def _download_agent_log(self, agent: Agent, machines: Mapping[MachineID, Machine]):
        log_file_path = self._get_log_file_path(agent, machines)
        log_contents = self.island_client.get_agent_log(agent.id)

        if log_contents:
            MonkeyLogsDownloader._write_log_to_file(log_file_path, log_contents)
            self.monkey_log_paths.append(log_file_path)

    def _download_island_log(self):
        log_contents = self.island_client.get_island_log()

        island_log_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dst_path = self.log_dir_path / f"island_{island_log_time}.log"

        if log_contents:
            log_contents = IslandLogParser(log_contents).filter_date(start=bb_singleton.start_time)
            MonkeyLogsDownloader._write_log_to_file(dst_path, log_contents)
            self.monkey_log_paths.append(dst_path)

    def _get_log_file_path(self, agent: Agent, machines: Mapping[MachineID, Machine]) -> Path:
        try:
            machine_ip = str(machines[agent.machine_id].network_interfaces[0].ip)
        except IndexError:
            logger.error(f"Machine with ID {agent.machine_id} has no network interfaces")
            machine_ip = "UNKNOWN"

        start_time = agent.start_time.strftime("%Y-%m-%d_%H-%M-%S")

        return self.log_dir_path / f"agent_{start_time}_{machine_ip}.log"

    @staticmethod
    def _write_log_to_file(log_file_path: Path, log_contents: str):
        logger.debug(f"Writing {len(log_contents)} bytes to {log_file_path}")

        with open(log_file_path, "w") as f:
            f.write(log_contents)

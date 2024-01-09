import logging
import multiprocessing
import time
from ipaddress import IPv4Interface
from typing import Any, Callable, Dict, List, Optional, Sequence

from egg_timer import EggTimer
from monkeytoolbox import create_daemon_thread, interruptible_iter

from infection_monkey.i_master import IMaster
from infection_monkey.i_puppet import IPuppet, RejectedRequestError
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIError
from infection_monkey.utils.propagation import maximum_depth_reached

from . import Exploiter, IPScanner, Propagator

CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC = 5
CHECK_FOR_TERMINATE_INTERVAL_SEC = CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC / 5
SHUTDOWN_TIMEOUT = 60
NUM_SCAN_THREADS = 16
NUM_EXPLOIT_THREADS = 6

logger = logging.getLogger()


class AutomatedMaster(IMaster):
    def __init__(
        self,
        current_depth: Optional[int],
        servers: Sequence[str],
        puppet: IPuppet,
        island_api_client: IIslandAPIClient,
        local_network_interfaces: List[IPv4Interface],
    ):
        self._current_depth = current_depth
        self._servers = servers
        self._puppet = puppet
        self._island_api_client = island_api_client

        ip_scanner = IPScanner(self._puppet, NUM_SCAN_THREADS)

        exploiter = Exploiter(self._puppet, NUM_EXPLOIT_THREADS)
        self._propagator = Propagator(
            ip_scanner,
            exploiter,
            local_network_interfaces,
        )

        multiprocessing_context = multiprocessing.get_context(method="spawn")
        self._stop = multiprocessing_context.Event()

        self._master_thread = create_daemon_thread(
            target=self._run_master_thread, name="AutomatedMasterThread"
        )
        self._simulation_thread = create_daemon_thread(
            target=self._run_simulation, name="SimulationThread"
        )

    def start(self):
        logger.info("Starting automated breach and attack simulation")
        self._master_thread.start()
        self._master_thread.join()
        logger.info("The simulation has been shutdown.")

    def terminate(self, block: bool = False):
        logger.info("Stopping automated breach and attack simulation")
        self._stop.set()

        if self._master_thread.is_alive() and block:
            self._master_thread.join()
            # We can only have confidence that the master terminated successfully if block is set
            # and join() has returned.
            logger.info("AutomatedMaster successfully terminated.")

    def _run_master_thread(self):
        self._simulation_thread.start()

        self._wait_for_master_stop_condition()

        logger.debug("Waiting for the simulation thread to stop")
        self._simulation_thread.join(SHUTDOWN_TIMEOUT)

        if self._simulation_thread.is_alive():
            logger.warning("Timed out waiting for the simulation to stop")
            # Since the master thread and all child threads are daemon threads, they will be
            # forcefully killed when the program exits.
            logger.warning("Forcefully killing the simulation")

    def _wait_for_master_stop_condition(self):
        logger.debug(
            "Checking for the stop signal from the island every "
            f"{CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC} seconds."
        )
        timer = EggTimer()
        timer.set(CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC)

        while self._master_thread_should_run():
            if timer.is_expired():
                self._check_for_stop()
                timer.reset()

            time.sleep(CHECK_FOR_TERMINATE_INTERVAL_SEC)

    def _check_for_stop(self):
        try:
            stop = self._island_api_client.terminate_signal_is_set()
            if stop:
                logger.info("Received the terminate signal from the Island")
                self._stop.set()
        except IslandAPIError as e:
            logger.error(f"An error occurred while trying to check for the terminate signal: {e}")
            self._stop.set()

    def _master_thread_should_run(self):
        return (not self._stop.is_set()) and self._simulation_thread.is_alive()

    def _run_simulation(self):
        try:
            config = self._island_api_client.get_config()
        except IslandAPIError as e:
            logger.error(f"An error occurred while fetching configuration: {e}")
            return

        credentials_collector_thread = create_daemon_thread(
            target=self._run_plugins,
            name="CredentialsCollectorThread",
            args=(
                config.credentials_collectors,
                "credentials collector",
                self._collect_credentials,
            ),
        )
        # We don't need to use multithreading here, but it's likely that in the
        # future we'll like to run other tasks while credentials are being collected
        credentials_collector_thread.start()
        credentials_collector_thread.join()

        current_depth = self._current_depth if self._current_depth is not None else 0
        logger.info(f"Current depth is {current_depth}")

        if not maximum_depth_reached(config.propagation.maximum_depth, current_depth):
            self._propagator.propagate(config.propagation, current_depth, self._servers, self._stop)
        else:
            logger.info("Skipping propagation: maximum depth reached")

        payload_thread = create_daemon_thread(
            target=self._run_plugins,
            name="PayloadThread",
            args=(config.payloads, "payload", self._run_payload),
        )
        payload_thread.start()
        payload_thread.join()

    def _collect_credentials(self, collector_name: str, collector_options: Dict[str, Any]):
        credentials = self._puppet.run_credentials_collector(
            collector_name, collector_options, self._stop
        )

        if not credentials:
            logger.debug(f"No credentials were collected by {collector_name}")

    def _run_payload(self, name: str, options: Dict):
        self._puppet.run_payload(name, options, self._stop)

    def _run_plugins(
        self,
        plugins: Dict[str, Dict],
        plugin_type: str,
        callback: Callable[[str, Dict], None],
    ):
        logger.info(f"Running {plugin_type}s")
        logger.debug(f"Found {len(plugins)} {plugin_type}(s) to run")

        interrupted_message = f"Received a stop signal, skipping remaining {plugin_type}s"
        for p in interruptible_iter(plugins, self._stop, interrupted_message):
            try:
                logger.info(f'Trying to run plugin "{p}" of type "{plugin_type}"')
                callback(p, plugins[p])
            except RejectedRequestError as err:
                logger.info(f"Skipping plugin {p} of type {plugin_type}: {err}")
                continue
            except Exception:
                logger.exception(
                    f"Got unhandled exception when running {plugin_type} plugin {p}. "
                    f"Plugin was passed to {callback}"
                )

        logger.info(f"Finished running {plugin_type}s")

    def cleanup(self):
        pass

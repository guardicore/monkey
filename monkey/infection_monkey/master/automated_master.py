import logging
import threading
import time
from ipaddress import IPv4Interface
from typing import Any, Callable, Collection, List, Optional, Sequence

from common.agent_configuration import CustomPBAConfiguration, PluginConfiguration
from common.utils import Timer
from infection_monkey.credential_repository import IPropagationCredentialsRepository
from infection_monkey.i_control_channel import IControlChannel, IslandCommunicationError
from infection_monkey.i_master import IMaster
from infection_monkey.i_puppet import IPuppet
from infection_monkey.model import VictimHostFactory
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils.propagation import maximum_depth_reached
from infection_monkey.utils.threading import create_daemon_thread, interruptible_iter

from . import Exploiter, IPScanner, Propagator
from .option_parsing import custom_pba_is_enabled

CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC = 5
CHECK_FOR_TERMINATE_INTERVAL_SEC = CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC / 5
SHUTDOWN_TIMEOUT = 5
NUM_SCAN_THREADS = 16
NUM_EXPLOIT_THREADS = 6
CHECK_FOR_STOP_AGENT_COUNT = 5
CHECK_FOR_CONFIG_COUNT = 3

logger = logging.getLogger()


class AutomatedMaster(IMaster):
    def __init__(
        self,
        current_depth: Optional[int],
        servers: Sequence[str],
        puppet: IPuppet,
        telemetry_messenger: ITelemetryMessenger,
        victim_host_factory: VictimHostFactory,
        control_channel: IControlChannel,
        local_network_interfaces: List[IPv4Interface],
        credentials_store: IPropagationCredentialsRepository,
    ):
        self._current_depth = current_depth
        self._servers = servers
        self._puppet = puppet
        self._telemetry_messenger = telemetry_messenger
        self._control_channel = control_channel

        ip_scanner = IPScanner(self._puppet, NUM_SCAN_THREADS)

        exploiter = Exploiter(self._puppet, NUM_EXPLOIT_THREADS, credentials_store.get_credentials)
        self._propagator = Propagator(
            self._telemetry_messenger,
            ip_scanner,
            exploiter,
            victim_host_factory,
            local_network_interfaces,
        )

        self._stop = threading.Event()
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
        timer = Timer()
        timer.set(CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC)

        while self._master_thread_should_run():
            if timer.is_expired():
                self._check_for_stop()
                timer.reset()

            time.sleep(CHECK_FOR_TERMINATE_INTERVAL_SEC)

    @staticmethod
    def _try_communicate_with_island(fn: Callable[[], Any], max_tries: int) -> Any:
        tries = 0
        while tries < max_tries:
            try:
                return fn()
            except IslandCommunicationError as e:
                tries += 1
                logger.debug(f"{e}. Retries left: {max_tries-tries}")
                if tries >= max_tries:
                    raise e

    def _check_for_stop(self):
        try:
            stop = AutomatedMaster._try_communicate_with_island(
                self._control_channel.should_agent_stop, CHECK_FOR_STOP_AGENT_COUNT
            )
            if stop:
                logger.info('Received the "stop" signal from the Island')
                self._stop.set()
        except IslandCommunicationError as e:
            logger.error(f"An error occurred while trying to check for agent stop: {e}")
            self._stop.set()

    def _master_thread_should_run(self):
        return (not self._stop.is_set()) and self._simulation_thread.is_alive()

    def _run_simulation(self):
        try:
            config = AutomatedMaster._try_communicate_with_island(
                self._control_channel.get_config, CHECK_FOR_CONFIG_COUNT
            )
        except IslandCommunicationError as e:
            logger.error(f"An error occurred while fetching configuration: {e}")
            return

        credential_collector_thread = create_daemon_thread(
            target=self._run_plugins,
            name="CredentialCollectorThread",
            args=(
                config.credential_collectors,
                "credential collector",
                self._collect_credentials,
            ),
        )
        pba_thread = create_daemon_thread(
            target=self._run_pbas,
            name="PBAThread",
            args=(config.post_breach_actions, self._run_pba, config.custom_pbas),
        )

        credential_collector_thread.start()
        pba_thread.start()

        # Future stages of the simulation require the output of the system info collectors. Nothing
        # requires the output of PBAs, so we don't need to join on that thread here. We will join on
        # the PBA thread later in this function to prevent the simulation from ending while PBAs are
        # still running.
        credential_collector_thread.join()

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

        pba_thread.join()

    def _collect_credentials(self, collector: PluginConfiguration):
        credentials = self._puppet.run_credential_collector(collector.name, collector.options)

        if not credentials:
            logger.debug(f"No credentials were collected by {collector}")

    def _run_pba(self, pba: PluginConfiguration):
        for pba_data in self._puppet.run_pba(pba.name, pba.options):
            self._telemetry_messenger.send_telemetry(PostBreachTelem(pba_data))

    def _run_payload(self, payload: PluginConfiguration):
        self._puppet.run_payload(payload.name, payload.options, self._stop)

    def _run_pbas(
        self,
        plugins: Collection[PluginConfiguration],
        callback: Callable[[Any], None],
        custom_pba_options: CustomPBAConfiguration,
    ):
        self._run_plugins(plugins, "post-breach action", callback)

        if custom_pba_is_enabled(custom_pba_options):
            self._run_plugins(
                [PluginConfiguration(name="CustomPBA", options=custom_pba_options.__dict__)],
                "post-breach action",
                callback,
            )

    def _run_plugins(
        self,
        plugins: Collection[PluginConfiguration],
        plugin_type: str,
        callback: Callable[[Any], None],
    ):
        logger.info(f"Running {plugin_type}s")
        logger.debug(f"Found {len(plugins)} {plugin_type}(s) to run")

        interrupted_message = f"Received a stop signal, skipping remaining {plugin_type}s"
        for p in interruptible_iter(plugins, self._stop, interrupted_message):
            try:
                callback(p)
            except Exception:
                logger.exception(
                    f"Got unhandled exception when running {plugin_type} plugin {p}. "
                    f"Plugin was passed to {callback}"
                )

        logger.info(f"Finished running {plugin_type}s")

    def cleanup(self):
        pass

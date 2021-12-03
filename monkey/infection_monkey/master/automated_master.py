import logging
import threading
import time
from typing import Dict, List

from infection_monkey.i_control_channel import IControlChannel
from infection_monkey.i_master import IMaster
from infection_monkey.i_puppet import IPuppet
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.telemetry.system_info_telem import SystemInfoTelem
from infection_monkey.utils.timer import Timer

CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC = 5
CHECK_FOR_TERMINATE_INTERVAL_SEC = CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC / 5
SHUTDOWN_TIMEOUT = 5

logger = logging.getLogger()


class AutomatedMaster(IMaster):
    def __init__(
        self,
        puppet: IPuppet,
        telemetry_messenger: ITelemetryMessenger,
        control_channel: IControlChannel,
    ):
        self._puppet = puppet
        self._telemetry_messenger = telemetry_messenger
        self._control_channel = control_channel

        self._stop = threading.Event()
        self._master_thread = threading.Thread(target=self._run_master_thread, daemon=True)
        self._simulation_thread = threading.Thread(target=self._run_simulation, daemon=True)

    def start(self):
        logger.info("Starting automated breach and attack simulation")
        self._master_thread.start()
        self._master_thread.join()
        logger.info("The simulation has been shutdown.")

    def terminate(self):
        logger.info("Stopping automated breach and attack simulation")
        self._stop.set()

        if self._master_thread.is_alive():
            self._master_thread.join()

    def _run_master_thread(self):
        self._simulation_thread.start()

        self._wait_for_master_stop_condition()

        logger.debug("Waiting for the simulation thread to stop")
        self._simulation_thread.join(SHUTDOWN_TIMEOUT)

        if self._simulation_thread.is_alive():
            logger.warning("Timed out waiting for the simulation to stop")
            # Since the master thread and all child threads are daemon threads, they will be
            # forcefully killed when the program exits.
            # TODO: Daemon threads to not die when the parent THREAD does, but when the parent
            #       PROCESS does. This could lead to conflicts between threads that refuse to die
            #       and the cleanup() function. Come up with a solution.
            logger.warning("Forcefully killing the simulation")

    def _wait_for_master_stop_condition(self):
        timer = Timer()
        timer.set(CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC)

        while self._master_thread_should_run():
            if timer.is_expired():
                # TODO: Handle exceptions in _check_for_stop() once
                #       ControlChannel.should_agent_stop() is refactored.
                self._check_for_stop()
                timer.reset()

            time.sleep(CHECK_FOR_TERMINATE_INTERVAL_SEC)

    def _check_for_stop(self):
        if self._control_channel.should_agent_stop():
            logger.debug('Received the "stop" signal from the Island')
            self._stop.set()

    def _master_thread_should_run(self):
        return (not self._stop.is_set()) and self._simulation_thread.is_alive()

    def _run_simulation(self):
        config = self._control_channel.get_config()

        system_info_collector_thread = threading.Thread(
            target=self._collect_system_info,
            args=(config["system_info_collector_classes"],),
            daemon=True,
        )
        pba_thread = threading.Thread(
            target=self._run_pbas, args=(config["post_breach_actions"],), daemon=True
        )

        system_info_collector_thread.start()
        pba_thread.start()

        # Future stages of the simulation require the output of the system info collectors. Nothing
        # requires the output of PBAs, so we don't need to join on that thread here. We will join on
        # the PBA thread later in this function to prevent the simulation from ending while PBAs are
        # still running.
        system_info_collector_thread.join()

        if self._can_propagate():
            propagation_thread = threading.Thread(
                target=self._propagate, args=(config,), daemon=True
            )
            propagation_thread.start()
            propagation_thread.join()

        payload_thread = threading.Thread(
            target=self._run_payloads, args=(config["payloads"],), daemon=True
        )
        payload_thread.start()
        payload_thread.join()

        pba_thread.join()

        # TODO: This code is just for testing in development. Remove when
        # 		implementation of AutomatedMaster is finished.
        while True:
            time.sleep(2)
            logger.debug("Simulation thread is finished sleeping")
            if self._stop.is_set():
                break

    def _collect_system_info(self, enabled_collectors: List[str]):
        logger.info("Running system info collectors")

        for collector in enabled_collectors:
            if self._stop.is_set():
                logger.debug("Received a stop signal, skipping remaining system info collectors")
                break

            logger.info(f"Running system info collector: {collector}")

            system_info_telemetry = {}
            system_info_telemetry[collector] = self._puppet.run_sys_info_collector(collector)
            self._telemetry_messenger.send_telemetry(
                SystemInfoTelem({"collectors": system_info_telemetry})
            )

        logger.info("Finished running system info collectors")

    def _run_pbas(self, enabled_pbas: List[str]):
        pass

    def _can_propagate(self):
        return True

    def _propagate(self, config: Dict):
        pass

    def _run_payloads(self, enabled_payloads: Dict[str, Dict]):
        logger.info("Running payloads")
        logger.debug(f"Found {len(enabled_payloads.keys())} payload(s) to run")

        for payload_name, options in enabled_payloads.items():
            if self._stop.is_set():
                logger.debug("Received a stop signal, skipping remaining system info collectors")
                break

            self._puppet.run_payload(payload_name, options, self._stop)

        logger.info("Finished running payloads")

    def cleanup(self):
        pass

import logging
import threading
import time
from typing import Dict, List

from infection_monkey.i_control_channel import IControlChannel
from infection_monkey.i_master import IMaster
from infection_monkey.i_puppet import IPuppet
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger

CHECK_FOR_STOP_INTERVAL_SEC = 5
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

    def start(self):
        logger.info("Starting automated breach and attack simulation")
        self._master_thread.start()
        self._master_thread.join()
        logger.info("The simulation has been shutdown.")

    def _check_for_stop(self):
        if self._control_channel.should_agent_stop():
            logger.debug('Received the "stop" signal from the Island')
            self._stop.set()

    def terminate(self):
        logger.info("Stopping automated breach and attack simulation")
        self._stop.set()

        if self._master_thread.is_alive():
            self._master_thread.join()

    def _run_master_thread(self):
        _simulation_thread = threading.Thread(target=self._run_simulation, daemon=True)
        _simulation_thread.start()

        while (not self._stop.is_set()) and _simulation_thread.is_alive():
            time.sleep(CHECK_FOR_STOP_INTERVAL_SEC)
            self._check_for_stop()

        logger.debug("Waiting for the simulation thread to stop")
        _simulation_thread.join(SHUTDOWN_TIMEOUT)

        if _simulation_thread.is_alive():
            logger.warn("Timed out waiting for the simulation to stop")
            # Since the master thread is a Daemon thread, it will be forcefully
            # killed when the program exits.
            logger.warn("Forcefully killing the simulation")

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
        # requires the output of PBAs, so we don't need to join on that thread.
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

        while True:
            time.sleep(2)
            logger.debug("Simulation thread is finished sleeping")
            if self._stop.is_set():
                break

    def _collect_system_info(self, enabled_collectors: List[str]):
        pass

    def _run_pbas(self, enabled_pbas: List[str]):
        pass

    def _can_propagate(self):
        return True

    def _propagate(self, config: Dict):
        pass

    def _run_payloads(self, enabled_payloads: Dict[str, Dict]):
        pass

    def cleanup(self):
        pass

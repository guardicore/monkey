import logging
import threading
import time

from infection_monkey.i_control_channel import IControlChannel
from infection_monkey.i_master import IMaster
from infection_monkey.i_puppet import IPuppet
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger

CHECK_FOR_STOP_INTERVAL_SEC = 5
SHUTDOWN_TIMEOUT = 2

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
        pass

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
        while True:
            time.sleep(30)
            logger.debug("Simulation thread is finished sleeping")
            if self._stop.is_set():
                break

    def cleanup(self):
        pass

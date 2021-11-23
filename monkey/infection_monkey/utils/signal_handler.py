import logging
import signal

from infection_monkey.i_master import IMaster
from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.exceptions.planned_shutdown_exception import PlannedShutdownException

logger = logging.getLogger(__name__)


class StopSignalHandler:
    def __init__(self, master: IMaster):
        self._master = master

    def __call__(self, _, __):
        self._master.terminate()
        logger.debug("Some kind of interrupt signal was sent to the Monkey Agent")
        raise PlannedShutdownException("Monkey Agent got an interrupt signal")


def register_signal_handlers(master: IMaster):
    stop_signal_handler = StopSignalHandler(master)
    signal.signal(signal.SIGINT, stop_signal_handler)
    signal.signal(signal.SIGTERM, stop_signal_handler)

    if is_windows_os():
        signal.signal(signal.SIGBREAK, stop_signal_handler)

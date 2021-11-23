import logging
import signal

from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.exceptions.planned_shutdown_exception import PlannedShutdownException

logger = logging.getLogger(__name__)


def stop_signal_handler(_, __):
    # IMaster.cleanup()
    logger.debug("Some kind of interrupt signal was sent to the Monkey Agent")
    raise PlannedShutdownException("Monkey Agent got an interrupt signal")


def register_signal_handlers():
    signal.signal(signal.SIGINT, stop_signal_handler)
    signal.signal(signal.SIGTERM, stop_signal_handler)

    if is_windows_os():
        signal.signal(signal.SIGBREAK, stop_signal_handler)

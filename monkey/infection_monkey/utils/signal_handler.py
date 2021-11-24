import logging
import signal

from infection_monkey.i_master import IMaster
from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.exceptions.planned_shutdown_exception import PlannedShutdownException

logger = logging.getLogger(__name__)


class StopSignalHandler:
    def __init__(self, master: IMaster):
        self._master = master

    def handle_posix_signals(self, signum, _):
        self._handle_signal(signum)
        # Windows signal handlers must return boolean. Only raising this exception for POSIX
        # signals.
        raise PlannedShutdownException("Monkey Agent got an interrupt signal")

    def handle_windows_signals(self, signum):
        import win32con

        # TODO: This signal handler gets called for a CTRL_CLOSE_EVENT, but the system immediately
        #       kills the process after the handler returns. After the master is implemented and the
        #       setup/teardown of the Agent is fully refactored, revisit this signal handler and
        #       modify as necessary to more gracefully handle CTRL_CLOSE_EVENT signals.
        if signum in {win32con.CTRL_C_EVENT, win32con.CTRL_BREAK_EVENT, win32con.CTRL_CLOSE_EVENT}:
            self._handle_signal(signum)
            return True

        return False

    def _handle_signal(self, signum):
        logger.info(f"The Monkey Agent received signal {signum}")
        self._master.terminate()


def register_signal_handlers(master: IMaster):
    stop_signal_handler = StopSignalHandler(master)

    if is_windows_os():
        import win32api

        # CTRL_CLOSE_EVENT signal has a timeout of 5000ms,
        # after that OS will forcefully kill the process
        win32api.SetConsoleCtrlHandler(stop_signal_handler.handle_windows_signals, True)
    else:
        signal.signal(signal.SIGINT, stop_signal_handler.handle_posix_signals)
        signal.signal(signal.SIGTERM, stop_signal_handler.handle_posix_signals)

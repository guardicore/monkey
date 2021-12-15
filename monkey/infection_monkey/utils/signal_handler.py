import logging
import signal

from infection_monkey.i_master import IMaster
from infection_monkey.utils.environment import is_windows_os

logger = logging.getLogger(__name__)


class StopSignalHandler:
    def __init__(self, master: IMaster):
        self._master = master

    def handle_posix_signals(self, signum: int, _):
        self._handle_signal(signum, False)

    def handle_windows_signals(self, signum: int):
        import win32con

        if signum in {win32con.CTRL_C_EVENT, win32con.CTRL_BREAK_EVENT}:
            self._handle_signal(signum, False)
            return True

        if signum == win32con.CTRL_CLOSE_EVENT:
            # After the signal handler returns True, the OS will forcefully kill the process.
            # Calling self._handle_signal() with block=True to give the master a chance to
            # gracefully shut down. Note that the OS has a timeout that will forcefully kill the
            # process if this handler hasn't returned in time.
            self._handle_signal(signum, True)
            return True

        return False

    def _handle_signal(self, signum: int, block: bool):
        logger.info(f"The Monkey Agent received signal {signum}")
        self._master.terminate(block)


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

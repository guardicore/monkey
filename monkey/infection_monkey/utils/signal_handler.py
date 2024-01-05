import logging
import signal
from typing import Optional

from monkeytoolbox import get_os
from monkeytypes import OperatingSystem

from infection_monkey.i_master import IMaster

logger = logging.getLogger(__name__)


_signal_handler = None


class StopSignalHandler:
    def __init__(self, master: IMaster):
        self._master = master

    # Windows won't let us correctly deregister a method, but Callables and closures work.
    def __call__(self, signum: int, *args) -> Optional[bool]:
        if get_os() == OperatingSystem.WINDOWS:
            return self._handle_windows_signals(signum)

        self._handle_posix_signals(signum, args)
        return None

    def _handle_windows_signals(self, signum: int) -> bool:
        import win32con

        if signum in {win32con.CTRL_C_EVENT, win32con.CTRL_BREAK_EVENT}:
            self._terminate_master(signum, False)
            return True

        if signum == win32con.CTRL_CLOSE_EVENT:
            # After the signal handler returns True, the OS will forcefully kill the process.
            # Calling self._handle_signal() with block=True to give the master a chance to
            # gracefully shut down. Note that the OS has a timeout that will forcefully kill the
            # process if this handler hasn't returned in time.
            self._terminate_master(signum, True)
            return True

        return False

    def _handle_posix_signals(self, signum: int, *_):
        self._terminate_master(signum, False)

    def _terminate_master(self, signum: int, block: bool):
        logger.info(f"The Monkey Agent received signal {signum}")
        self._master.terminate(block)


def register_signal_handlers(master: IMaster):
    global _signal_handler
    _signal_handler = StopSignalHandler(master)

    if get_os() == OperatingSystem.WINDOWS:
        import win32api

        # CTRL_CLOSE_EVENT signal has a timeout of 5000ms,
        # after that OS will forcefully kill the process
        win32api.SetConsoleCtrlHandler(_signal_handler, True)
    else:
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)


def reset_signal_handlers():
    """
    Resets the signal handlers back to the default handlers provided by Python
    """
    global _signal_handler

    if get_os() == OperatingSystem.WINDOWS:
        import win32api

        if _signal_handler:
            win32api.SetConsoleCtrlHandler(_signal_handler, False)
    else:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

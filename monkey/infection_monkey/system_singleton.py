import ctypes
import logging
import sys
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


SINGLETON_MUTEX_NAME = "{2384ec59-0df8-4ab9-918c-843740924a28}"


class _SystemSingleton(object, metaclass=ABCMeta):
    @abstractmethod
    def try_lock(self):
        raise NotImplementedError()

    @abstractmethod
    def unlock(self):
        raise NotImplementedError()


class WindowsSystemSingleton(_SystemSingleton):
    def __init__(self):
        self._mutex_name = r"Global\%s" % (SINGLETON_MUTEX_NAME,)
        self._mutex_handle = None

    def try_lock(self):
        assert self._mutex_handle is None, "Singleton already locked"

        handle = ctypes.windll.kernel32.CreateMutexA(
            None, ctypes.c_bool(True), ctypes.c_char_p(self._mutex_name.encode())
        )
        last_error = ctypes.windll.kernel32.GetLastError()

        if not handle:
            logger.error(
                "Cannot acquire system singleton %r, unknown error %d", self._mutex_name, last_error
            )
            return False
        if winerror.ERROR_ALREADY_EXISTS == last_error:
            logger.debug(
                "Cannot acquire system singleton %r, mutex already exist", self._mutex_name
            )
            return False

        self._mutex_handle = handle
        logger.debug("Global singleton mutex %r acquired", self._mutex_name)

        return True

    def unlock(self):
        assert self._mutex_handle is not None, "Singleton not locked"
        ctypes.windll.kernel32.CloseHandle(self._mutex_handle)
        self._mutex_handle = None


class LinuxSystemSingleton(_SystemSingleton):
    def __init__(self):
        self._unix_sock_name = str(SINGLETON_MUTEX_NAME)
        self._sock_handle = None

    def try_lock(self):
        assert self._sock_handle is None, "Singleton already locked"

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        try:
            sock.bind("\0" + self._unix_sock_name)
        except socket.error as e:
            logger.error(
                "Cannot acquire system singleton %r, error code %d, error: %s",
                self._unix_sock_name,
                e.args[0],
                e.args[1],
            )
            return False

        self._sock_handle = sock

        logger.debug("Global singleton mutex %r acquired", self._unix_sock_name)

        return True

    def unlock(self):
        assert self._sock_handle is not None, "Singleton not locked"
        self._sock_handle.close()
        self._sock_handle = None


if sys.platform == "win32":
    import winerror

    SystemSingleton = WindowsSystemSingleton
else:
    import socket

    SystemSingleton = LinuxSystemSingleton

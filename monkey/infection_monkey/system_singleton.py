import ctypes
import logging
import sys
from abc import ABCMeta, abstractmethod

from infection_monkey.config import WormConfiguration

__author__ = 'itamar'

LOG = logging.getLogger(__name__)


class _SystemSingleton(object, metaclass=ABCMeta):
    @property
    @abstractmethod
    def locked(self):
        raise NotImplementedError()

    @abstractmethod
    def try_lock(self):
        raise NotImplementedError()

    @abstractmethod
    def unlock(self):
        raise NotImplementedError()


class WindowsSystemSingleton(_SystemSingleton):
    def __init__(self):
        self._mutex_name = r"Global\%s" % (WormConfiguration.singleton_mutex_name,)
        self._mutex_handle = None

    @property
    def locked(self):
        return self._mutex_handle is not None

    def try_lock(self):
        assert self._mutex_handle is None, "Singleton already locked"

        handle = ctypes.windll.kernel32.CreateMutexA(None,
                                                     ctypes.c_bool(True),
                                                     ctypes.c_char_p(self._mutex_name.encode()))
        last_error = ctypes.windll.kernel32.GetLastError()

        if not handle:
            LOG.error("Cannot acquire system singleton %r, unknown error %d",
                      self._mutex_name, last_error)
            return False
        if winerror.ERROR_ALREADY_EXISTS == last_error:
            LOG.debug("Cannot acquire system singleton %r, mutex already exist",
                      self._mutex_name)
            return False

        self._mutex_handle = handle
        LOG.debug("Global singleton mutex %r acquired",
                  self._mutex_name)

        return True

    def unlock(self):
        assert self._mutex_handle is not None, "Singleton not locked"
        ctypes.windll.kernel32.CloseHandle(self._mutex_handle)
        self._mutex_handle = None


class LinuxSystemSingleton(_SystemSingleton):
    def __init__(self):
        self._unix_sock_name = str(WormConfiguration.singleton_mutex_name)
        self._sock_handle = None

    @property
    def locked(self):
        return self._sock_handle is not None

    def try_lock(self):
        assert self._sock_handle is None, "Singleton already locked"

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        try:
            sock.bind('\0' + self._unix_sock_name)
        except socket.error as e:
            LOG.error("Cannot acquire system singleton %r, error code %d, error: %s",
                      self._unix_sock_name, e.args[0], e.args[1])
            return False

        self._sock_handle = sock

        LOG.debug("Global singleton mutex %r acquired", self._unix_sock_name)

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

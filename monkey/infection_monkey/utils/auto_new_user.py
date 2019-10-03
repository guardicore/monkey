import logging
import abc

from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.linux.users import AutoNewLinuxUser
from infection_monkey.utils.windows.users import AutoNewWindowsUser

logger = logging.getLogger(__name__)


class NewUserError(Exception):
    pass


class AutoNewUser:
    """
    RAII object to use for creating and using a new user. Use with `with`.
    User will be created when the instance is instantiated.
    User will be available for use (log on for Windows, for example) at the start of the `with` scope.
    User will be removed (deactivated and deleted for Windows, for example) at the end of said `with` scope.

    Example:
             # Created                                                 # Logged on
        with AutoNewUser("user", "pass", is_on_windows()) as new_user:
            ...
            ...
        # Logged off and deleted
        ...
        """
    __metaclass__ = abc.ABCMeta

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()


def create_auto_new_user(username, password, is_windows=is_windows_os()):
    """
    Factory method for creating an AutoNewUser. See AutoNewUser's documentation for more information.
    Example usage:
        with create_auto_new_user(username, PASSWORD) as new_user:
            ...
    :param username: The username of the new user.
    :param password: The password of the new user.
    :param is_windows: If True, a new Windows user is created. Otherwise, a Linux user is created. Leave blank for
    automatic detection.
    :return: The new AutoNewUser object - use with a `with` scope.
    """
    if is_windows:
        return AutoNewWindowsUser(username, password)
    else:
        return AutoNewLinuxUser(username, password)



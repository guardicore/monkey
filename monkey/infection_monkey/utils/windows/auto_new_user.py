import logging
import subprocess
import abc

from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.linux.users import get_linux_commands_to_add_user, get_linux_commands_to_delete_user
from infection_monkey.utils.windows.users import get_windows_commands_to_delete_user, get_windows_commands_to_add_user, \
    get_windows_commands_to_deactivate_user

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
        raise NotImplementedError()

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()


def create_auto_new_user(username, password, is_windows=is_windows_os()):
    if is_windows:
        return AutoNewWindowsUser(username, password)
    else:
        return AutoNewLinuxUser(username, password)


class AutoNewLinuxUser(AutoNewUser):
    """
    See AutoNewUser's documentation for details.
    """
    def __init__(self, username, password):
        """
        Creates a user with the username + password.
        :raises: subprocess.CalledProcessError if failed to add the user.
        """
        super(AutoNewLinuxUser, self).__init__(username, password)
        self.username = username
        self.password = password

        commands_to_add_user = get_linux_commands_to_add_user(username)
        logger.debug("Trying to add {} with commands {}".format(self.username, str(commands_to_add_user)))
        _ = subprocess.check_output(' '.join(commands_to_add_user), stderr=subprocess.STDOUT, shell=True)

    def __enter__(self):
        pass  # No initialization/logging on needed in Linux

    def __exit__(self, exc_type, exc_val, exc_tb):
        # delete the user.
        commands_to_delete_user = get_linux_commands_to_delete_user(self.username)
        logger.debug("Trying to delete {} with commands {}".format(self.username, str(commands_to_delete_user)))
        _ = subprocess.check_output(" ".join(commands_to_delete_user), stderr=subprocess.STDOUT, shell=True)


class AutoNewWindowsUser(AutoNewUser):
    """
    See AutoNewUser's documentation for details.
    """
    def __init__(self, username, password):
        """
        Creates a user with the username + password.
        :raises: subprocess.CalledProcessError if failed to add the user.
        """
        super(AutoNewWindowsUser, self).__init__(username, password)
        self.username = username
        self.password = password

        windows_cmds = get_windows_commands_to_add_user(self.username, self.password, True)
        _ = subprocess.check_output(windows_cmds, stderr=subprocess.STDOUT, shell=True)

    def __enter__(self):
        # Importing these only on windows, as they won't exist on linux.
        import win32security
        import win32con

        try:
            # Logon as new user: https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-logonusera
            self.logon_handle = win32security.LogonUser(
                self.username,
                ".",  # Use current domain.
                self.password,
                win32con.LOGON32_LOGON_INTERACTIVE,  # Logon type - interactive (normal user). Need this to open ping
                                                     # using a shell.
                win32con.LOGON32_PROVIDER_DEFAULT)  # Which logon provider to use - whatever Windows offers.
        except Exception as err:
            raise NewUserError("Can't logon as {}. Error: {}".format(self.username, str(err)))
        return self

    def get_logon_handle(self):
        return self.logon_handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Logoff
        self.logon_handle.Close()

        # Try to disable and then delete the user.
        self.try_deactivate_user()
        self.try_delete_user()

    def try_deactivate_user(self):
        try:
            _ = subprocess.check_output(
                get_windows_commands_to_deactivate_user(self.username), stderr=subprocess.STDOUT, shell=True)
        except Exception as err:
            raise NewUserError("Can't deactivate user {}. Info: {}".format(self.username, err))

    def try_delete_user(self):
        try:
            _ = subprocess.check_output(
                get_windows_commands_to_delete_user(self.username), stderr=subprocess.STDOUT, shell=True)
        except Exception as err:
            raise NewUserError("Can't delete user {}. Info: {}".format(self.username, err))

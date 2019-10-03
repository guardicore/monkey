import logging
import subprocess

from infection_monkey.post_breach.actions.add_user import BackdoorUser
from infection_monkey.utils.windows.users import get_windows_commands_to_delete_user, get_windows_commands_to_add_user, \
    get_windows_commands_to_deactivate_user

logger = logging.getLogger(__name__)


class NewUserError(Exception):
    pass


class AutoNewUser(object):
    """
    RAII object to use for creating and using a new user in Windows. Use with `with`.
    User will be created when the instance is instantiated.
    User will log on at the start of the `with` scope.
    User will log off and get deleted at the end of said `with` scope.

    Example:
             # Created                           # Logged on
        with AutoNewUser("user", "pass") as new_user:
            ...
            ...
        # Logged off and deleted
        ...
    """
    def __init__(self, username, password):
        """
        Creates a user with the username + password.
        :raises: subprocess.CalledProcessError if failed to add the user.
        """
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
        self.try_disable_user()

    def try_disable_user(self):
        try:
            _ = subprocess.check_output(
                get_windows_commands_to_delete_user(self.username), stderr=subprocess.STDOUT, shell=True)
        except Exception as err:
            raise NewUserError("Can't delete user {}. Info: {}".format(self.username, err))

    def try_deactivate_user(self):
        try:
            _ = subprocess.check_output(
                get_windows_commands_to_deactivate_user(self.username), stderr=subprocess.STDOUT, shell=True)
        except Exception as err:
            raise NewUserError("Can't deactivate user {}. Info: {}".format(self.username, err))

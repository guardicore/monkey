import logging
import subprocess

from infection_monkey.post_breach.actions.add_user import BackdoorUser
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem


logger = logging.getLogger(__name__)


class NewUserError(Exception):
    pass


class NewUser(object):
    """
    RAII object to use for creating and using a new user in Windows. Use with `with`.
    User will be created when the instance is instantiated.
    User will log on start of `with` scope.
    User will log off on end of `with` scope.

    Example:
             # Created                           # Logged on
        with NewUser("user", "pass") as new_user:
            ...
            ...
        # Logged off
        ...
    """
    def __init__(self, username, password):
        """
        Creates a user with the username + password.
        :raises: subprocess.CalledProcessError if failed to add the user.
        """
        self.username = username
        self.password = password

        windows_cmds = BackdoorUser.get_windows_commands_to_add_user(self.username, self.password, True)
        logger.debug("Trying these commands: {}".format(str(windows_cmds)))
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
                win32con.LOGON32_LOGON_INTERACTIVE,  # Logon type - interactive (normal user).
                win32con.LOGON32_PROVIDER_DEFAULT)  # Which logon provider to use - whatever Windows offers.
        except Exception as err:
            raise NewUserError("Can't logon as {}. Error: {}".format(self.username, str(err)))
        return self

    def get_logon_handle(self):
        return self.logon_handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logon_handle.Close()
        # TODO Delete user

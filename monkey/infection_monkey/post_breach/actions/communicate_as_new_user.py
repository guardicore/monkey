import logging
import os
import random
import string
import subprocess

from common.data.post_breach_consts import POST_BREACH_COMMUNICATE_AS_NEW_USER
from infection_monkey.post_breach.actions.add_user import BackdoorUser
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils import is_windows_os

CREATED_PROCESS_AS_USER_WINDOWS_FORMAT = "Created process '{}' as user '{}'."
CREATED_PROCESS_AS_USER_LINUX_FORMAT = "Created process '{}' as user '{}'. Some of the output was '{}'."

USERNAME = "somenewuser"
PASSWORD = "N3WPa55W0rD!1"

logger = logging.getLogger(__name__)


class CommunicateAsNewUser(PBA):
    """
    This PBA creates a new user, and then pings google as that user. This is used for a Zero Trust test of the People
    pillar. See the relevant telemetry processing to see what findings are created.
    """

    def __init__(self):
        super(CommunicateAsNewUser, self).__init__(name=POST_BREACH_COMMUNICATE_AS_NEW_USER)

    def run(self):
        username = USERNAME + ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        if is_windows_os():
            if not self.try_to_create_user_windows(username, PASSWORD):
                return  # no point to continue if failed creating the user.

            try:
                # Importing these only on windows, as they won't exist on linux.
                import win32con
                import win32process
                import win32security
                # Logon as new user: https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-logonusera
                new_user_logon_token_handle = win32security.LogonUser(
                    username,
                    ".",  # use current domain
                    PASSWORD,
                    win32con.LOGON32_LOGON_INTERACTIVE,  # logon type - interactive (normal user)
                    win32con.LOGON32_PROVIDER_DEFAULT)  # logon provider
            except Exception as e:
                PostBreachTelem(
                    self,
                    ("Can't logon as {}. Error: {}".format(username, e.message), False)
                ).send()
                return  # no point to continue if can't log on.

            # Using os.path is OK, as this is on windows for sure
            ping_app_path = os.path.join(os.environ["WINDIR"], "system32", "PING.exe")
            if not os.path.exists(ping_app_path):
                PostBreachTelem(self, ("{} not found.".format(ping_app_path), False)).send()
                return  # Can't continue without ping.

            try:
                # Open process as that user:
                # https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasusera
                commandline = "{} {}".format(ping_app_path, "google.com")
                _ = win32process.CreateProcessAsUser(
                    new_user_logon_token_handle,  # A handle to the primary token that represents a user.
                    None,  # The name of the module to be executed.
                    commandline,  # The command line to be executed.
                    None,  # Process attributes
                    None,  # Thread attributes
                    True,  # Should inherit handles
                    win32con.NORMAL_PRIORITY_CLASS,  # The priority class and the creation of the process.
                    None,  # An environment block for the new process. If this parameter is NULL, the new process
                    # uses the environment of the calling process.
                    None,  # CWD. If this parameter is NULL, the new process will have the same current drive and
                    # directory as the calling process.
                    win32process.STARTUPINFO()  # STARTUPINFO structure.
                    # https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfoa
                )

                PostBreachTelem(self, (
                    CREATED_PROCESS_AS_USER_WINDOWS_FORMAT.format(commandline, username), True)).send()
                return
            except Exception as e:
                # TODO: if failed on 1314, we can try to add elevate the rights of the current user with the "Replace a
                #  process level token" right, using Local Security Policy editing. Worked, but only after reboot. So:
                #  1. need to decide if worth it, and then
                #  2. need to find how to do this using python...
                PostBreachTelem(self, (
                    "Failed to open process as user {}. Error: {}".format(username, str(e)), False)).send()
                return
        else:
            try:
                linux_cmds = BackdoorUser.get_linux_commands_to_add_user(username)
                commandline = "'ping -c 2 google.com'"
                linux_cmds.extend([";", "sudo", "-u", username, commandline])
                final_command = ' '.join(linux_cmds)
                logger.debug("Trying to execute these commands: {}".format(final_command))
                output = subprocess.check_output(final_command, stderr=subprocess.STDOUT, shell=True)
                PostBreachTelem(self, (
                    CREATED_PROCESS_AS_USER_LINUX_FORMAT.format(commandline, username, output[:50]), True)).send()
                return
            except subprocess.CalledProcessError as e:
                PostBreachTelem(self, (e.output, False)).send()
                return

    def try_to_create_user_windows(self, username, password):
        try:
            windows_cmds = BackdoorUser.get_windows_commands_to_add_user(username, password, True)
            logger.debug("Trying these commands: {}".format(str(windows_cmds)))
            subprocess.check_output(windows_cmds, stderr=subprocess.STDOUT, shell=True)
            return True
        except subprocess.CalledProcessError as e:
            PostBreachTelem(self, (
                "Couldn't create the user '{}'. Error output is: '{}'".format(username, e.output), False)).send()
            return False

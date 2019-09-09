import logging
import os
import random
import string
import subprocess
import time

from common.data.post_breach_consts import POST_BREACH_COMMUNICATE_AS_NEW_USER
from infection_monkey.monkey_utils.windows.new_user import NewUser, NewUserError
from infection_monkey.post_breach.actions.add_user import BackdoorUser
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils import is_windows_os

PING_TEST_DOMAIN = "google.com"

PING_WAIT_TIMEOUT_IN_SECONDS = 20

CREATED_PROCESS_AS_USER_PING_SUCCESS_FORMAT = "Created process '{}' as user '{}', and successfully pinged."
CREATED_PROCESS_AS_USER_PING_FAILED_FORMAT = "Created process '{}' as user '{}', but failed to ping (exit status {})."

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
            self.communicate_as_new_user_windows(username)
        else:
            self.communicate_as_new_user_linux(username)

    def communicate_as_new_user_linux(self, username):
        try:
            # add user + ping
            linux_cmds = BackdoorUser.get_linux_commands_to_add_user(username)
            commandline = "ping -c 1 {}".format(PING_TEST_DOMAIN)
            linux_cmds.extend([";", "sudo", "-u", username, commandline])
            final_command = ' '.join(linux_cmds)
            exit_status = os.system(final_command)
            self.send_ping_result_telemetry(exit_status, commandline, username)
            # delete the user
            _ = subprocess.check_output(
                BackdoorUser.get_linux_commands_to_delete_user(username), stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            PostBreachTelem(self, (e.output, False)).send()

    def communicate_as_new_user_windows(self, username):
        # Importing these only on windows, as they won't exist on linux.
        import win32con
        import win32process
        import win32api

        try:
            with NewUser(username, PASSWORD) as new_user:
                # Using os.path is OK, as this is on windows for sure
                ping_app_path = os.path.join(os.environ["WINDIR"], "system32", "PING.exe")
                if not os.path.exists(ping_app_path):
                    PostBreachTelem(self, ("{} not found.".format(ping_app_path), False)).send()
                    return  # Can't continue without ping.

                try:
                    # Open process as that user:
                    # https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasusera
                    commandline = "{} {} {} {}".format(ping_app_path, PING_TEST_DOMAIN, "-n", "1")
                    process_info = win32process.CreateProcessAsUser(
                        new_user.get_logon_handle(),  # A handle to the primary token that represents a user.
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

                    ping_exit_code = win32process.GetExitCodeProcess(process_info[0])
                    counter = 0
                    while ping_exit_code == win32con.STILL_ACTIVE and counter < PING_WAIT_TIMEOUT_IN_SECONDS:
                        ping_exit_code = win32process.GetExitCodeProcess(process_info[0])
                        counter += 1
                        logger.debug("Waiting for ping to finish, round {}. Exit code: {}".format(counter, ping_exit_code))
                        time.sleep(1)

                    self.send_ping_result_telemetry(ping_exit_code, commandline, username)

                    win32api.CloseHandle(process_info[0])  # Process handle
                    win32api.CloseHandle(process_info[1])  # Thread handle

                except Exception as e:
                    # TODO: if failed on 1314, we can try to add elevate the rights of the current user with the
                    #  "Replace a process level token" right, using Local Security Policy editing. Worked, but only
                    #  after reboot. So:
                    #  1. need to decide if worth it, and then
                    #  2. need to find how to do this using python...
                    PostBreachTelem(self, (
                        "Failed to open process as user {}. Error: {}".format(username, str(e)), False)).send()
        except subprocess.CalledProcessError as err:
            PostBreachTelem(self, (
                "Couldn't create the user '{}'. Error output is: '{}'".format(username, str(err)),
                False)).send()
        except NewUserError as e:
            PostBreachTelem(self, (str(e), False)).send()

    def send_ping_result_telemetry(self, exit_status, commandline, username):
        if exit_status == 0:
            PostBreachTelem(self, (
                CREATED_PROCESS_AS_USER_PING_SUCCESS_FORMAT.format(commandline, username), True)).send()
        else:
            PostBreachTelem(self, (
                CREATED_PROCESS_AS_USER_PING_FAILED_FORMAT.format(commandline, username, exit_status), False)).send()

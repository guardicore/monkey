import logging
import os
import random
import string
import subprocess

from infection_monkey.utils.auto_new_user import NewUserError, create_auto_new_user
from common.data.post_breach_consts import POST_BREACH_COMMUNICATE_AS_NEW_USER
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils.environment import is_windows_os

PING_TEST_DOMAIN = "google.com"

PING_WAIT_TIMEOUT_IN_MILLISECONDS = 20 * 1000

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
        username = CommunicateAsNewUser.get_random_new_user_name()
        if is_windows_os():
            self.communicate_as_new_user_windows(username)
        else:
            self.communicate_as_new_user_linux(username)

    @staticmethod
    def get_random_new_user_name():
        return USERNAME + ''.join(random.choice(string.ascii_lowercase) for _ in range(5))

    def communicate_as_new_user_linux(self, username):
        try:
            with create_auto_new_user(username, PASSWORD, is_windows=False) as _:
                commandline = "sudo -u {username} ping -c 1 {domain}".format(
                    username=username,
                    domain=PING_TEST_DOMAIN)
                exit_status = os.system(commandline)
                self.send_ping_result_telemetry(exit_status, commandline, username)
        except subprocess.CalledProcessError as e:
            PostBreachTelem(self, (e.output, False)).send()

    def communicate_as_new_user_windows(self, username):
        # Importing these only on windows, as they won't exist on linux.
        import win32con
        import win32process
        import win32api
        import win32event

        try:
            with create_auto_new_user(username, PASSWORD, is_windows=True) as new_user:
                # Using os.path is OK, as this is on windows for sure
                ping_app_path = os.path.join(os.environ["WINDIR"], "system32", "PING.exe")
                if not os.path.exists(ping_app_path):
                    PostBreachTelem(self, ("{} not found.".format(ping_app_path), False)).send()
                    return  # Can't continue without ping.

                try:
                    # Open process as that user:
                    # https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasusera
                    commandline = "{} {} {} {}".format(ping_app_path, PING_TEST_DOMAIN, "-n", "1")
                    process_handle, thread_handle, _, _ = win32process.CreateProcessAsUser(
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

                    logger.debug(
                        "Waiting for ping process to finish. Timeout: {}ms".format(PING_WAIT_TIMEOUT_IN_MILLISECONDS))

                    # Ignoring return code, as we'll use `GetExitCode` to determine the state of the process later.
                    _ = win32event.WaitForSingleObject(  # Waits until the specified object is signaled, or time-out.
                        process_handle,  # Ping process handle
                        PING_WAIT_TIMEOUT_IN_MILLISECONDS  # Timeout in milliseconds
                    )

                    ping_exit_code = win32process.GetExitCodeProcess(process_handle)

                    self.send_ping_result_telemetry(ping_exit_code, commandline, username)
                except Exception as e:
                    # If failed on 1314, it's possible to try to elevate the rights of the current user with the
                    #  "Replace a process level token" right, using Local Security Policy editing.
                    PostBreachTelem(self, (
                        "Failed to open process as user {}. Error: {}".format(username, str(e)), False)).send()
                finally:
                    try:
                        win32api.CloseHandle(process_handle)
                        win32api.CloseHandle(thread_handle)
                    except Exception as err:
                        logger.error("Close handle error: " + str(err))
        except subprocess.CalledProcessError as err:
            PostBreachTelem(self, (
                "Couldn't create the user '{}'. Error output is: '{}'".format(username, str(err)),
                False)).send()
        except NewUserError as e:
            PostBreachTelem(self, (str(e), False)).send()

    def send_ping_result_telemetry(self, exit_status, commandline, username):
        """
        Parses the result of ping and sends telemetry accordingly.

        :param exit_status: In both Windows and Linux, 0 exit code from Ping indicates success.
        :param commandline: Exact commandline which was executed, for reporting back.
        :param username: Username from which the command was executed, for reporting back.
        """
        if exit_status == 0:
            PostBreachTelem(self, (
                CREATED_PROCESS_AS_USER_PING_SUCCESS_FORMAT.format(commandline, username), True)).send()
        else:
            PostBreachTelem(self, (
                CREATED_PROCESS_AS_USER_PING_FAILED_FORMAT.format(commandline, username, exit_status), False)).send()

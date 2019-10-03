import logging
import os
import random
import string
import subprocess

from infection_monkey.utils.new_user_error import NewUserError
from infection_monkey.utils.auto_new_user_factory import create_auto_new_user
from common.data.post_breach_consts import POST_BREACH_COMMUNICATE_AS_NEW_USER
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils.environment import is_windows_os

PING_TEST_DOMAIN = "google.com"

CREATED_PROCESS_AS_USER_PING_SUCCESS_FORMAT = "Created process '{}' as user '{}', and successfully pinged."
CREATED_PROCESS_AS_USER_PING_FAILED_FORMAT = "Created process '{}' as user '{}', but failed to ping (exit status {})."

USERNAME_PREFIX = "somenewuser"
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
        try:
            with create_auto_new_user(username, PASSWORD) as new_user:
                ping_commandline = CommunicateAsNewUser.get_commandline_for_ping()
                exit_status = new_user.run_as(ping_commandline)
                self.send_ping_result_telemetry(exit_status, ping_commandline, username)
        except subprocess.CalledProcessError as e:
            PostBreachTelem(self, (e.output, False)).send()
        except NewUserError as e:
            PostBreachTelem(self, (str(e), False)).send()

    @staticmethod
    def get_random_new_user_name():
        return USERNAME_PREFIX + ''.join(random.choice(string.ascii_lowercase) for _ in range(5))

    @staticmethod
    def get_commandline_for_ping(domain=PING_TEST_DOMAIN, is_windows=is_windows_os()):
        format_string = "PING.exe {domain} -n 1" if is_windows else "ping -c 1 {domain}"
        format_string.format(domain=domain)

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

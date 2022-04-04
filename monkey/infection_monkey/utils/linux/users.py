import datetime
import logging
import shlex
import subprocess

from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
from infection_monkey.utils.auto_new_user import AutoNewUser

logger = logging.getLogger(__name__)


def get_linux_commands_to_add_user(username):
    return [
        "useradd",  # https://linux.die.net/man/8/useradd
        "-M",  # Do not create homedir
        "--expiredate",  # The date on which the user account will be disabled.
        datetime.datetime.today().strftime("%Y-%m-%d"),
        # The number of days after a password expires until the account is permanently disabled.
        "--inactive",
        "0",  # A value of 0 disables the account as soon as the password has expired
        "-c",  # Comment
        "MONKEY_USER",  # Comment
        username,
    ]


def get_linux_commands_to_delete_user(username):
    return ["deluser", username]


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

        commands_to_add_user = get_linux_commands_to_add_user(username)
        logger.debug(
            "Trying to add {} with commands {}".format(self.username, str(commands_to_add_user))
        )
        try:
            _ = subprocess.check_output(
                commands_to_add_user, stderr=subprocess.STDOUT, timeout=SHORT_REQUEST_TIMEOUT
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
            logger.error(f"An exception occurred when creating a new linux user: {str(err)}")

    def __enter__(self):
        return self  # No initialization/logging on needed in Linux

    def run_as(self, command):
        command_as_new_user = shlex.split(
            "sudo -u {username} {command}".format(username=self.username, command=command)
        )
        try:
            return subprocess.call(command_as_new_user, timeout=SHORT_REQUEST_TIMEOUT)
        except subprocess.TimeoutExpired as err:
            logger.error(
                f"An exception occurred when running a command as a new linux user: {str(err)}"
            )

    def __exit__(self, _exc_type, value, traceback):
        # delete the user.
        commands_to_delete_user = get_linux_commands_to_delete_user(self.username)
        logger.debug(
            "Trying to delete {} with commands {}".format(
                self.username, str(commands_to_delete_user)
            )
        )
        try:
            _ = subprocess.check_output(
                commands_to_delete_user, stderr=subprocess.STDOUT, timeout=SHORT_REQUEST_TIMEOUT
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
            logger.error(f"An exception occurred when deleting the new linux user: {str(err)}")

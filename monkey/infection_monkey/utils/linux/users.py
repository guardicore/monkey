import datetime
import logging
import os
import subprocess

from infection_monkey.utils.auto_new_user import AutoNewUser

logger = logging.getLogger(__name__)


def get_linux_commands_to_add_user(username):
    return [
        'useradd',  # https://linux.die.net/man/8/useradd
        '-M',  # Do not create homedir
        '--expiredate',  # The date on which the user account will be disabled.
        datetime.datetime.today().strftime('%Y-%m-%d'),
        '--inactive',  # The number of days after a password expires until the account is permanently disabled.
        '0',  # A value of 0 disables the account as soon as the password has expired
        '-c',  # Comment
        'MONKEY_USER',  # Comment
        username]


def get_linux_commands_to_delete_user(username):
    return [
        'deluser',
        username
    ]


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
        logger.debug("Trying to add {} with commands {}".format(self.username, str(commands_to_add_user)))
        _ = subprocess.check_output(' '.join(commands_to_add_user), stderr=subprocess.STDOUT, shell=True)

    def __enter__(self):
        return self  # No initialization/logging on needed in Linux

    def run_as(self, command):
        command_as_new_user = "sudo -u {username} {command}".format(username=self.username, command=command)
        return os.system(command_as_new_user)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # delete the user.
        commands_to_delete_user = get_linux_commands_to_delete_user(self.username)
        logger.debug("Trying to delete {} with commands {}".format(self.username, str(commands_to_delete_user)))
        _ = subprocess.check_output(" ".join(commands_to_delete_user), stderr=subprocess.STDOUT, shell=True)

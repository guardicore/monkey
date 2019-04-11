import datetime
import logging
import subprocess
import sys
from infection_monkey.config import WormConfiguration

LOG = logging.getLogger(__name__)

# Linux doesn't have WindowsError
try:
    WindowsError
except NameError:
    WindowsError = None

__author__ = 'danielg'


class BackdoorUser(object):
    """
    This module adds a disabled user to the system.
    This tests part of the ATT&CK matrix
    """

    def act(self):
        LOG.info("Adding a user")
        try:
            if sys.platform.startswith("win"):
                retval = self.add_user_windows()
            else:
                retval = self.add_user_linux()
            if retval != 0:
                LOG.warn("Failed to add a user")
            else:
                LOG.info("Done adding user")
        except OSError:
            LOG.exception("Exception while adding a user")

    @staticmethod
    def add_user_linux():
        cmd_line = ['useradd', '-M', '--expiredate',
                    datetime.datetime.today().strftime('%Y-%m-%d'), '--inactive', '0', '-c', 'MONKEY_USER',
                    WormConfiguration.user_to_add]
        retval = subprocess.call(cmd_line)
        return retval

    @staticmethod
    def add_user_windows():
        cmd_line = ['net', 'user', WormConfiguration.user_to_add,
                    WormConfiguration.remote_user_pass,
                    '/add', '/ACTIVE:NO']
        retval = subprocess.call(cmd_line)
        return retval

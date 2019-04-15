import logging
import infection_monkey.config
from file_execution import FileExecution
from pba import PBA
from infection_monkey.utils import is_windows_os
from infection_monkey.utils import get_monkey_dir_path

LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'

DIR_CHANGE_WINDOWS = 'cd %s & '
DIR_CHANGE_LINUX = 'cd %s ; '


class PostBreach(object):
    """
    This class handles post breach actions execution
    """
    def __init__(self):
        self.os_is_linux = not is_windows_os()
        self.pba_list = self.config_to_pba_list(infection_monkey.config.WormConfiguration)

    def execute(self):
        """
        Executes all post breach actions.
        """
        for pba in self.pba_list:
            pba.run(self.os_is_linux)
        LOG.info("Post breach actions executed")

    @staticmethod
    def config_to_pba_list(config):
        """
        Returns a list of PBA objects generated from config.
        :param config: Monkey configuration
        :return: A list of PBA objects.
        """
        pba_list = []
        pba_list.extend(PostBreach.get_custom_PBA(config))

        return pba_list

    @staticmethod
    def get_custom_PBA(config):
        """
        Creates post breach actions depending on users input into 'custom post breach' config section
        :param config: monkey's configuration
        :return: List of PBA objects ([user's file execution PBA, user's command execution PBA])
        """
        custom_list = []
        file_pba = FileExecution()
        command_pba = PBA(name="Custom")

        if not is_windows_os():
            # Add linux commands to PBA's
            if config.PBA_linux_filename:
                if config.custom_PBA_linux_cmd:
                    # Add change dir command, because user will try to access his file
                    file_pba.linux_command = (DIR_CHANGE_LINUX % get_monkey_dir_path()) + config.custom_PBA_linux_cmd
                else:
                    file_pba.add_default_command(is_linux=True)
            elif config.custom_PBA_linux_cmd:
                command_pba.linux_command = config.custom_PBA_linux_cmd
        else:
            # Add windows commands to PBA's
            if config.PBA_windows_filename:
                if config.custom_PBA_windows_cmd:
                    # Add change dir command, because user will try to access his file
                    file_pba.windows_command = (DIR_CHANGE_WINDOWS % get_monkey_dir_path()) + \
                                               config.custom_PBA_windows_cmd
                else:
                    file_pba.add_default_command(is_linux=False)
            elif config.custom_PBA_windows_cmd:
                command_pba.windows_command = config.custom_PBA_windows_cmd

        # Add PBA's to list
        if file_pba.linux_command or file_pba.windows_command:
            custom_list.append(file_pba)
        if command_pba.windows_command or command_pba.linux_command:
            custom_list.append(command_pba)

        return custom_list

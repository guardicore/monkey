import logging
import infection_monkey.config
import platform
from file_execution import FileExecution
from pba import PBA

LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'


# Class that handles post breach action execution
class PostBreach(object):
    def __init__(self):
        self.os_is_linux = False if platform.system() == 'Windows' else True
        self.pba_list = self.config_to_pba_list(infection_monkey.config.WormConfiguration)

    def execute(self):
        for pba in self.pba_list:
            pba.run(self.os_is_linux)
        LOG.info("Post breach actions executed")

    @staticmethod
    def config_to_pba_list(config):
        """
        Returns a list of PBA objects generated from config.
        """
        pba_list = []
        pba_list.extend(PostBreach.get_custom(config))

        return pba_list

    @staticmethod
    def get_custom(config):
        custom_list = []
        file_pba = FileExecution()
        command_pba = PBA(name="Custom")
        post_breach = config.custom_post_breach
        linux_command = post_breach['linux']
        windows_command = post_breach['windows']

        # Add commands to linux pba
        if post_breach['linux_file_info']['name']:
            if linux_command:
                file_pba.linux_command=linux_command
            else:
                file_pba.add_default_command(is_linux=True)
        elif linux_command:
            command_pba.linux_command = linux_command

        # Add commands to windows pba
        if post_breach['windows_file_info']['name']:
            if windows_command:
                file_pba.windows_command=windows_command
            else:
                file_pba.add_default_command(is_linux=False)
        elif windows_command:
            command_pba.windows_command = windows_command

        # Add pba's to list
        if file_pba.linux_command or file_pba.windows_command:
            custom_list.append(file_pba)
        if command_pba.windows_command or command_pba.linux_command:
            custom_list.append(command_pba)

        return custom_list

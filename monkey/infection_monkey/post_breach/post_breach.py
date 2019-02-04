import logging
import infection_monkey.config
import subprocess
import platform

LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'


# Class that handles post breach action execution
class PostBreach(object):
    def __init__(self):
        self.pba_list = PostBreach.config_to_pba_list(infection_monkey.config.WormConfiguration)

    def execute(self):
        for pba in self.pba_list:
            if platform.system() == 'Windows':
                return pba.execute_win()
            else:
                return pba.execute_linux()

    @staticmethod
    def config_to_pba_list(config):
        """
        Should return a list of PBA's generated from config. After ATT&CK is implemented this will pick
        which PBA's to run.
        """
        pba_list = []
        # Get custom PBA command from config
        custom_pba_linux = config.post_breach_actions['linux'] if "linux" in config.post_breach_actions else ""
        custom_pba_windows = config.post_breach_actions['windows'] if "windows" in config.post_breach_actions else ""

        if custom_pba_linux or custom_pba_windows:
            pba_list.append(PBA(custom_pba_linux, custom_pba_windows))
        return pba_list


# Post Breach Action container
class PBA(object):
    def __init__(self, linux_command="", windows_command=""):
        self.linux_command = linux_command
        self.windows_command = windows_command

    def execute_linux(self):
        return subprocess.check_output(self.linux_command, shell=True) if self.linux_command else False

    def execute_win(self):
        return subprocess.check_output(self.windows_command, shell=True) if self.windows_command else False


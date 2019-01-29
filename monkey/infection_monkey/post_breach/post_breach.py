import logging
import infection_monkey.config
import subprocess
from abc import abstractmethod

LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'


# Class that handles post breach action execution
class PostBreach(object):
    def __init__(self, host, pba_list):
        self._config = infection_monkey.config.WormConfiguration
        self.pba_list = pba_list
        self.host = host

    def execute(self):
        for pba in self.pba_list:
            if self.host.is_linux():
                pba.execute_linux()
            else:
                pba.execute_win()

    @staticmethod
    @abstractmethod
    def config_to_pba_list(config):
        """
        Should return a list of PBA's generated from config
        """
        raise NotImplementedError()


# Post Breach Action container
class PBA(object):
    def __init__(self, linux_command="", windows_command=""):
        self.linux_command = linux_command
        self.windows_command = windows_command

    def execute_linux(self):
        return subprocess.check_output(self.linux_command, shell=True)

    def execute_win(self):
        return subprocess.check_output(self.windows_command, shell=True)


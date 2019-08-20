import logging
import subprocess

from common.utils.attack_utils import ScanStatus
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils import is_windows_os
from infection_monkey.config import WormConfiguration
from infection_monkey.telemetry.attack.t1064_telem import T1064Telem


LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'


class PBA(object):
    """
    Post breach action object. Can be extended to support more than command execution on target machine.
    """
    def __init__(self, name="unknown", linux_cmd="", windows_cmd=""):
        """
        :param name: Name of post breach action.
        :param command: Command that will be executed on breached machine
        """
        self.command = PBA.choose_command(linux_cmd, windows_cmd)
        self.name = name

    def get_pba(self):
        """
        This method returns a PBA object based on a worm's configuration.
        Return None or False if you don't want the pba to be executed.
        :return: A pba object.
        """
        return self

    @staticmethod
    def should_run(class_name):
        """
        Decides if post breach action is enabled in config
        :return: True if it needs to be ran, false otherwise
        """
        return class_name in WormConfiguration.post_breach_actions

    def run(self):
        """
        Runs post breach action command
        """
        exec_funct = self._execute_default
        result = exec_funct()
        if self.scripts_were_used(result):
            T1064Telem(ScanStatus.USED, "Scripts used to execute %s post breach action." % self.name).send()
        PostBreachTelem(self, result).send()

    def scripts_were_used(self, pba_execution_result):
        """
        Determines if scripts were used to execute PBA
        :param pba_execution_result: result of execution function. e.g. self._execute_default
        :return: True if scripts were used, False otherwise
        """
        pba_execution_succeeded = pba_execution_result[1]
        if pba_execution_succeeded and isinstance(self.command, list) and len(self.command) > 1:
            return True
        return False

    def _execute_default(self):
        """
        Default post breach command execution routine
        :return: Tuple of command's output string and boolean, indicating if it succeeded
        """
        try:
            return subprocess.check_output(self.command, stderr=subprocess.STDOUT, shell=True), True
        except subprocess.CalledProcessError as e:
            # Return error output of the command
            return e.output, False

    @staticmethod
    def choose_command(linux_cmd, windows_cmd):
        """
        Helper method that chooses between linux and windows commands.
        :param linux_cmd:
        :param windows_cmd:
        :return: Command for current os
        """
        return windows_cmd if is_windows_os() else linux_cmd

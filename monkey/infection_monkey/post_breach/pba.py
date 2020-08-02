import logging
import subprocess

import infection_monkey.post_breach.actions
from common.utils.attack_utils import ScanStatus
from infection_monkey.config import WormConfiguration
from infection_monkey.telemetry.attack.t1064_telem import T1064Telem
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.plugins.plugin import Plugin

LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'


class PBA(Plugin):
    """
    Post breach action object. Can be extended to support more than command execution on target machine.
    """

    @staticmethod
    def base_package_name():
        return infection_monkey.post_breach.actions.__package__

    @staticmethod
    def base_package_file():
        return infection_monkey.post_breach.actions.__file__

    def __init__(self, name="unknown", linux_cmd="", windows_cmd=""):
        """
        :param name: Name of post breach action.
        :param linux_cmd: Command that will be executed on breached machine
        :param windows_cmd: Command that will be executed on breached machine
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
        if self.command:
            exec_funct = self._execute_default
            result = exec_funct()
            if self.scripts_were_used_successfully(result):
                T1064Telem(ScanStatus.USED, f"Scripts were used to execute {self.name} post breach action.").send()
            PostBreachTelem(self, result).send()
        else:
            LOG.debug(f"No command available for PBA '{self.name}' on current OS, skipping.")

    def is_script(self):
        """
        Determines if PBA is a script (PBA might be a single command)
        :return: True if PBA is a script(series of OS commands)
        """
        return isinstance(self.command, list) and len(self.command) > 1

    def scripts_were_used_successfully(self, pba_execution_result):
        """
        Determines if scripts were used to execute PBA and if they succeeded
        :param pba_execution_result: result of execution function. e.g. self._execute_default
        :return: True if scripts were used, False otherwise
        """
        pba_execution_succeeded = pba_execution_result[1]
        return pba_execution_succeeded and self.is_script()

    def _execute_default(self):
        """
        Default post breach command execution routine
        :return: Tuple of command's output string and boolean, indicating if it succeeded
        """
        try:
            output = subprocess.check_output(self.command, stderr=subprocess.STDOUT, shell=True).decode()
            return output, True
        except subprocess.CalledProcessError as e:
            # Return error output of the command
            return e.output.decode(), False

    @staticmethod
    def choose_command(linux_cmd, windows_cmd):
        """
        Helper method that chooses between linux and windows commands.
        :param linux_cmd:
        :param windows_cmd:
        :return: Command for current os
        """
        return windows_cmd if is_windows_os() else linux_cmd

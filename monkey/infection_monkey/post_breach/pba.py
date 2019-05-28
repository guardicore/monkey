import logging
import subprocess
from infection_monkey.control import ControlClient
from infection_monkey.utils import is_windows_os
from infection_monkey.config import WormConfiguration, GUID


LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'


class PBA(object):
    """
    Post breach action object. Can be extended to support more than command execution on target machine.
    """
    def __init__(self, name="unknown", command=""):
        """
        :param name: Name of post breach action.
        :param command: Command that will be executed on breached machine
        """
        self.command = command
        self.name = name

    @staticmethod
    def get_pba():
        """
        Should be overridden by all child classes.
        This method returns a PBA object based on worm's configuration.
        :return: An array of PBA objects.
        """
        raise NotImplementedError()

    @staticmethod
    def default_get_pba(name, pba_class, linux_cmd="", windows_cmd=""):
        """
        Default get_pba() method implementation
        :param name: PBA name
        :param pba_class: class instance. Class's name is matched to config to determine
        if corresponding field was enabled in post breach array or not.
        :param linux_cmd: commands for linux
        :param windows_cmd: commands for windows
        :return: post breach action
        """
        if pba_class.__name__ in WormConfiguration.post_breach_actions:
            command = PBA.choose_command(linux_cmd, windows_cmd)
            if command:
                return PBA(name, command)

    def run(self):
        """
        Runs post breach action command
        """
        exec_funct = self._execute_default
        result = exec_funct()
        ControlClient.send_telemetry('post_breach', {'command': self.command,
                                                     'result': result,
                                                     'name': self.name,
                                                     'guid': GUID})

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

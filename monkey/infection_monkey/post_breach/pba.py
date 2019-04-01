import logging
from infection_monkey.control import ControlClient
import subprocess
import socket

LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'


class PBA(object):
    """
    Post breach action object. Can be extended to support more than command execution on target machine.
    """
    def __init__(self, name="unknown", linux_command="", windows_command=""):
        """
        :param name: Name of post breach action.
        :param linux_command: Command that will be executed on linux machine
        :param windows_command: Command that will be executed on windows machine
        """
        self.linux_command = linux_command
        self.windows_command = windows_command
        self.name = name

    def run(self, is_linux):
        """
        Runs post breach action command
        :param is_linux: boolean that indicates on which os monkey is running
        """
        if is_linux:
            command = self.linux_command
            exec_funct = self._execute_linux
        else:
            command = self.windows_command
            exec_funct = self._execute_win
        if command:
            hostname = socket.gethostname()
            ControlClient.send_telemetry('post_breach', {'command': command,
                                                         'result': exec_funct(),
                                                         'name': self.name,
                                                         'hostname': hostname,
                                                         'ip': socket.gethostbyname(hostname)
                                                         })

    def _execute_linux(self):
        """
        Default linux PBA execution function. Override it if additional functionality is needed
        """
        return self._execute_default(self.linux_command)

    def _execute_win(self):
        """
        Default linux PBA execution function. Override it if additional functionality is needed
        """
        return self._execute_default(self.windows_command)

    @staticmethod
    def _execute_default(command):
        """
        Default post breach command execution routine
        :param command: What command to execute
        :return: Tuple of command's output string and boolean, indicating if it succeeded
        """
        try:
            return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True), True
        except subprocess.CalledProcessError as e:
            # Return error output of the command
            return e.output, False

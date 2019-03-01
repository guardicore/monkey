import logging
from infection_monkey.control import ControlClient
import subprocess

LOG = logging.getLogger(__name__)


# Post Breach Action container
class PBA(object):
    def __init__(self, name="unknown", linux_command="", windows_command=""):
        self.linux_command = linux_command
        self.windows_command = windows_command
        self.name = name

    def run(self, is_linux):
        if is_linux:
            command = self.linux_command
            exec_funct = self.execute_linux
        else:
            command = self.windows_command
            exec_funct = self.execute_win
        if command:
            ControlClient.send_telemetry('post_breach', {'command': command,
                                                         'output': exec_funct(),
                                                         'name': self.name})

    def execute_linux(self):
        # Default linux PBA execution function. Override if additional functionality is needed
        if self.linux_command:
            try:
                return subprocess.check_output(self.linux_command, stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError as e:
                # Return error output of the command
                return e.output

    def execute_win(self):
        # Default windows PBA execution function. Override if additional functionality is needed
        if self.windows_command:
            try:
                return subprocess.check_output(self.windows_command, stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError as e:
                # Return error output of the command
                return e.output

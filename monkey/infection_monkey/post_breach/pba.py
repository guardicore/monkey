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
        try:
            ControlClient.send_telemetry('post_breach', {'command': command,
                                                         'output': exec_funct(),
                                                         'name': self.name})
            return True
        except subprocess.CalledProcessError as e:
            ControlClient.send_telemetry('post_breach', {'command': command,
                                                         'output': "Couldn't execute post breach command: %s" % e,
                                                         'name': self.name})
            LOG.error("Couldn't execute post breach command: %s" % e)
            return False

    def execute_linux(self):
        return subprocess.check_output(self.linux_command, shell=True) if self.linux_command else False

    def execute_win(self):
        return subprocess.check_output(self.windows_command, shell=True) if self.windows_command else False

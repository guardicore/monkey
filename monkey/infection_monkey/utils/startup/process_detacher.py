import logging
import argparse
import subprocess

from infection_monkey.utils.environment import is_windows_os
from infection_monkey.exploit.tools.helpers import build_monkey_commandline_explicitly
from infection_monkey.model import MONKEY_CMDLINE_WINDOWS, MONKEY_CMDLINE_LINUX, GENERAL_CMDLINE_LINUX

if is_windows_os():
    from win32process import DETACHED_PROCESS
else:
    DETACHED_PROCESS = 0

LOG = logging.getLogger(__name__)


class MonkeyProcessDetacher:

    def __init__(self, flags: argparse.Namespace, destination_path):
        self._flags = flags
        self._destination_path = destination_path

    def detach_process(self) -> subprocess.Popen:
        monkey_options = build_monkey_commandline_explicitly(self._flags.parent,
                                                             self._flags.tunnel,
                                                             self._flags.server,
                                                             self._flags.depth)

        if is_windows_os():
            monkey_cmdline = MONKEY_CMDLINE_WINDOWS % {'monkey_path': self._destination_path} + monkey_options
        else:
            # In linux we have a more complex commandline. There's a general outer one, and the inner one which actually
            # runs the monkey
            inner_monkey_cmdline = MONKEY_CMDLINE_LINUX % {'monkey_filename': self._destination_path.split("/")[-1]} + \
                                   monkey_options
            monkey_cmdline = GENERAL_CMDLINE_LINUX % {'monkey_directory': self._form_monkey_directory_path(),
                                                      'monkey_commandline': inner_monkey_cmdline}

        monkey_process = subprocess.Popen(monkey_cmdline, shell=True,
                                          stdin=None, stdout=None, stderr=None,
                                          close_fds=True, creationflags=DETACHED_PROCESS)
        LOG.info("Executed monkey process (PID=%d) with command line: %s", monkey_process.pid, monkey_cmdline)
        return monkey_process

    def _form_monkey_directory_path(self):
        return self._destination_path[0:self._destination_path.rfind("/")]

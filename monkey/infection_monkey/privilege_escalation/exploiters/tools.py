import logging
import subprocess
import os

__author__ = 'D3fa1t'

LOG = logging.getLogger(__name__)
PGREP = "pgrep %(process_name)s -u 0"


def is_sudo_paswordless():
    LOG.info("Checking if monkey can execute paswordless sudo:")
    try:
        if b'sudo_test' in subprocess.check_output('echo ""| sudo -S echo "sudo_test"', shell=True):
            LOG.info("Monkey can run sudo without providing password!")
            return True
    except subprocess.CalledProcessError:
        LOG.info("Paswordless sudo not configured for current user.")
        return False


def shell(cmd):
    """
    To run the command on the shell and to read the output.
    :param cmd: The commands to be run on the shell
    :return: returns the output
    """
    try:
        result = subprocess.check_output(cmd)[:-1]
        return result
    except OSError:
        LOG.error("Can't read from the shell!")
        return False


def is_current_process_root():
    return os.geteuid() == 0


def run_monkey_as_root(command_line: str) -> bool:
    command_line = "sudo " + command_line
    monkey_process = subprocess.Popen(command_line, shell=True,
                                      stdin=None, stdout=None, stderr=None,
                                      close_fds=True, creationflags=0)

    LOG.info("Executed monkey process as root with (PID=%d) with command line: %s",
             monkey_process.pid, command_line)
    return True

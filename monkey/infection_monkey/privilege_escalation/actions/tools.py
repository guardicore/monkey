'''
Contains functions helpful for pe module
'''

import logging
import platform
import subprocess
import os
from pwd import getpwuid
__author__ = 'D3fa1t'

LOG = logging.getLogger(__name__)
PGREP = "pgrep %(process_name)s -u 0"


def check_if_sudoer(file):
    """
    see if the current user is a sudoers by checking if they are a part of the group monkey .

    :return: True if he is a sudoer, false if not
    """
    try:
        uname = getpwuid(os.stat(file).st_uid).pw_name
    except:
        LOG.info("The file was not created!")
        return False

    if "root" in uname:
        return True

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
    except OSError as e:
        LOG.error("Can't read from the shell!")
        return False


def check_if_running_as_root(pname):
    """
    Returns true if the monkey process is running as root
    :param pname: name of the monkey process
    :return:
    """
    if shell(PGREP % {'process_name': pname}):
        return True
    return False


def run_monkey_as_root(command_line):
    """"
    This function runs the monkey with the command line with root privilege
    :param command_line: monkey command line
    :return:
    """
    command_line = "sudo " + command_line
    monkey_process = subprocess.Popen(command_line, shell=True,
                                      stdin=None, stdout=None, stderr=None,
                                      close_fds=True, creationflags=0)

    LOG.info("Executed monkey process as root with (PID=%d) with command line: %s",
             monkey_process.pid, command_line)


# Commands needed for PE
REMOVE_LASTLINE = "sudo sed -i '$ d' %(file_name)s"
ADDUSER_TO_SUDOERS = "echo '%(user_name)s ALL = NOPASSWD: ALL' | sudo tee -a /etc/sudoers"
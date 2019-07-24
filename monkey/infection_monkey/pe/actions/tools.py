'''
Contains functions helpful for pe module
'''

import logging
import platform
import os
from pwd import getpwuid
__author__ = 'D3fa1t'

LOG = logging.getLogger(__name__)


PGREP = "pgrep %(process_name)s -u 0"

def check_if_sudoer(file):
    """
    see if the current user is a sudoer by checking if they are a part of the group monkey .

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


def check_system(properties):
    """
    Returns weather if the exploit can be run on the system
    :param properties: list containing (distro, os)
    :return:
    """
    uname = [x.lower() for x in platform.uname()]
    if set(properties).issubset(set(uname)):
        return True
    return False


def shell(cmd):
    """
    To run the command on the shell and to read the output.
    :param cmd: The commands to be run on the shell
    :return: returns the output
    """
    try:
        result = os.popen(cmd).read()[:-1]
        return result
    except OSError as e:
        LOG.error("Can't read from the shell!")
        return False


def check_running(pname):
    """
    Returns true if the monkey process is running as root
    :param pname: name of the monkey process
    :return:
    """
    if shell(PGREP %{'process_name': pname}):
        return True
    return False

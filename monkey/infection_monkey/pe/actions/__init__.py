from abc import ABCMeta, abstractmethod
from os.path import dirname, basename, isfile, join
import glob

__author__ = 'D3fa1t'

class HostPrivExploiter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def try_priv_esc(self,commad):
        raise NotImplementedError()

    def send_pe_telemetry(self, result, local_ip):
        from infection_monkey.control import ControlClient
        ControlClient.send_telemetry('pe', {'result': result, 'pe_name': self.__class__.__name__, 'ip': local_ip})


def get_pe_files():
    """
        Gets all files under current directory(/actions)
        :return: list of all files without .py ending
        """
    exclude_files = ('__init__.py','tools.py')
    files = glob.glob(join(dirname("__file__"), "*.py"))
    return [basename(f)[:-3] for f in files if isfile(f) and not f.endswith(exclude_files)]

from infection_monkey.pe.snapd import snapdExploiter
from infection_monkey.pe.ptrace_scope import ptraceScopeExploiter
from infection_monkey.pe.exim-CVE-2019-10149 import eximExploiter

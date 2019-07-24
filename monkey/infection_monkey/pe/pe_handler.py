import logging
import inspect
import importlib
from infection_monkey.pe.actions import get_pe_files
from infection_monkey.network.info import local_ips



LOG = logging.getLogger(__name__)

__author__ = 'D3fa1t'

PATH_TO_ACTIONS = "infection_monkey.pe.actions."

class PrivilegeEscalation(object):
    """
    This class handles privilege escalation execution
    """
    def __init__(self, command_line):
        self.pe_list = self.get_pe_list()
        self.command_line = command_line

    def execute(self):
        """
        Execute all pe classes one by one and if any succeeds then sends the telem data and returns true
        """
        for pe in self.pe_list:
            if pe().try_priv_esc(self.command_line):
                local_ip = local_ips()
                pe.send_pe_telemetry(True, str(local_ip))
                return True
        return False

    @staticmethod
    def get_pe_list():
        """
        Get the list of all the pe exploiter class from /actions
        :return: A list of Pe class .
        """
        pe_list = []
        pe_file_list = get_pe_files()
        for pe in pe_file_list:
            module = importlib.import_module(PATH_TO_ACTIONS + pe)
            pe_classes = [m[1] for m in inspect.getmembers(module, inspect.isclass) if
                          (m[1].__module__ == module.__name__)]

            for pe_class in pe_classes:
                pe_list.append(pe_class)

        return pe_list



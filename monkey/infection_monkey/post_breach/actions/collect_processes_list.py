import logging

import psutil

from common.common_consts.post_breach_consts import POST_BREACH_PROCESS_LIST_COLLECTION
from infection_monkey.post_breach.pba import PBA

logger = logging.getLogger(__name__)

# Linux doesn't have WindowsError
applicable_exceptions = psutil.AccessDenied
try:
    applicable_exceptions = (psutil.AccessDenied, WindowsError)
except NameError:
    pass


class ProcessListCollection(PBA):
    def __init__(self):
        super().__init__(POST_BREACH_PROCESS_LIST_COLLECTION)

    def run(self):
        """
        Collects process information from the host.
        Currently lists process name, ID, parent ID, command line
        and the full image path of each process.
        """
        logger.debug("Reading process list")

        processes = {}
        success_state = False
        for process in psutil.process_iter():
            try:
                processes[process.pid] = {
                    "name": process.name(),
                    "pid": process.pid,
                    "ppid": process.ppid(),
                    "cmdline": " ".join(process.cmdline()),
                    "full_image_path": process.exe(),
                }
                success_state = True
            except applicable_exceptions:
                # We may be running as non root and some processes are impossible to acquire in
                # Windows/Linux. In this case, we'll just add what we know.
                processes[process.pid] = {
                    "name": "null",
                    "pid": process.pid,
                    "ppid": process.ppid(),
                    "cmdline": "ACCESS DENIED",
                    "full_image_path": "null",
                }
                continue

        return self.command, [str(processes), success_state]

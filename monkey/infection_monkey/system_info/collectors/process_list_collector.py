import logging

import psutil

from common.data.system_info_collectors_names import PROCESS_LIST_COLLECTOR
from infection_monkey.system_info.system_info_collector import \
    SystemInfoCollector

logger = logging.getLogger(__name__)

# Linux doesn't have WindowsError
try:
    WindowsError
except NameError:
    # noinspection PyShadowingBuiltins
    WindowsError = psutil.AccessDenied


class ProcessListCollector(SystemInfoCollector):
    def __init__(self):
        super().__init__(name=PROCESS_LIST_COLLECTOR)

    def collect(self) -> dict:
        """
        Adds process information from the host to the system information.
        Currently lists process name, ID, parent ID, command line
        and the full image path of each process.
        """
        logger.debug("Reading process list")
        processes = {}
        for process in psutil.process_iter():
            try:
                processes[process.pid] = {
                    "name": process.name(),
                    "pid": process.pid,
                    "ppid": process.ppid(),
                    "cmdline": " ".join(process.cmdline()),
                    "full_image_path": process.exe(),
                }
            except (psutil.AccessDenied, WindowsError):
                # we may be running as non root and some processes are impossible to acquire in Windows/Linux.
                # In this case we'll just add what we know.
                processes[process.pid] = {
                    "name": "null",
                    "pid": process.pid,
                    "ppid": process.ppid(),
                    "cmdline": "ACCESS DENIED",
                    "full_image_path": "null",
                }
                continue

        return {'process_list': processes}

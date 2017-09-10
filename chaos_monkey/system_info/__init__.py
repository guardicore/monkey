import sys
import socket
import psutil
from enum import IntEnum
from network.info import get_host_subnets, local_ips

__author__ = 'uri'


class OperatingSystem(IntEnum):
    Windows = 0
    Linux = 1


class SystemInfoCollector(object):
    """
    A class that checks the current operating system and calls system information collecting modules accordingly
    """

    def __init__(self):
        self.os = SystemInfoCollector.get_os()
        if OperatingSystem.Windows == self.os:
            from windows_info_collector import WindowsInfoCollector
            self.collector = WindowsInfoCollector()
        else:
            from linux_info_collector import LinuxInfoCollector
            self.collector = LinuxInfoCollector()

    def get_info(self):
        return self.collector.get_info()

    @staticmethod
    def get_os():
        if sys.platform.startswith("win"):
            return OperatingSystem.Windows
        else:
            return OperatingSystem.Linux


class InfoCollector(object):
    """
    Generic Info Collection module
    """

    def __init__(self):
        self.info = {}

    def get_hostname(self):
        self.info['hostname'] = socket.gethostname()

    def get_process_list(self):
        processes = {}
        for process in psutil.process_iter():
            try:
                processes[process.pid] = {"name": process.name(),
                                          "pid": process.pid,
                                          "ppid": process.ppid(),
                                          "cmdline": " ".join(process.cmdline()),
                                          "full_image_path": process.exe(),
                                          }
            except psutil.AccessDenied:
                # we may be running as non root
                # and some processes are impossible to acquire in Windows/Linux
                # in this case we'll just add what we can
                processes[process.pid] = {"name": "null",
                                          "pid": process.pid,
                                          "ppid": process.ppid(),
                                          "cmdline": "ACCESS DENIED",
                                          "full_image_path": "null",
                                          }
                pass
        self.info['process_list'] = processes

    def get_network_info(self):
        self.info['network'] = {'subnets': get_host_subnets(), 'local_ips': local_ips()}

import logging
import socket
import sys

import psutil
from enum import IntEnum

from infection_monkey.network.info import get_host_subnets
from infection_monkey.system_info.aws_collector import AwsCollector
from infection_monkey.system_info.azure_cred_collector import AzureCollector
from infection_monkey.system_info.netstat_collector import NetstatCollector

LOG = logging.getLogger(__name__)

# Linux doesn't have WindowsError
try:
    WindowsError
except NameError:
    # noinspection PyShadowingBuiltins
    WindowsError = psutil.AccessDenied

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
            from .windows_info_collector import WindowsInfoCollector
            self.collector = WindowsInfoCollector()
        else:
            from .linux_info_collector import LinuxInfoCollector
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

    def get_info(self):
        self.get_hostname()
        self.get_process_list()
        self.get_network_info()
        self.get_azure_info()
        self.get_aws_info()

    def get_hostname(self):
        """
        Adds the fully qualified computer hostname to the system information.
        :return: None. Updates class information
        """
        LOG.debug("Reading hostname")
        self.info['hostname'] = socket.getfqdn()

    def get_process_list(self):
        """
        Adds process information from the host to the system information.
        Currently lists process name, ID, parent ID, command line
        and the full image path of each process.
        :return: None. Updates class information
        """
        LOG.debug("Reading process list")
        processes = {}
        for process in psutil.process_iter():
            try:
                processes[process.pid] = {"name": process.name(),
                                          "pid": process.pid,
                                          "ppid": process.ppid(),
                                          "cmdline": " ".join(process.cmdline()),
                                          "full_image_path": process.exe(),
                                          }
            except (psutil.AccessDenied, WindowsError):
                # we may be running as non root
                # and some processes are impossible to acquire in Windows/Linux
                # in this case we'll just add what we can
                processes[process.pid] = {"name": "null",
                                          "pid": process.pid,
                                          "ppid": process.ppid(),
                                          "cmdline": "ACCESS DENIED",
                                          "full_image_path": "null",
                                          }
                continue

        self.info['process_list'] = processes

    def get_network_info(self):
        """
        Adds network information from the host to the system information.
        Currently updates with netstat and a list of networks accessible from host
        containing host ip and the subnet range
        :return: None. Updates class information
        """
        LOG.debug("Reading subnets")
        self.info['network_info'] = \
            {
                'networks': get_host_subnets(),
                'netstat': NetstatCollector.get_netstat_info()
            }

    def get_azure_info(self):
        """
        Adds credentials possibly stolen from an Azure VM instance (if we're on one)
        Updates the credentials structure, creating it if necessary (compat with mimikatz)
        :return: None. Updates class information
        """
        # noinspection PyBroadException
        try:
            from infection_monkey.config import WormConfiguration
            if not WormConfiguration.extract_azure_creds:
                return
            LOG.debug("Harvesting creds if on an Azure machine")
            azure_collector = AzureCollector()
            if 'credentials' not in self.info:
                self.info["credentials"] = {}
            azure_creds = azure_collector.extract_stored_credentials()
            for cred in azure_creds:
                username = cred[0]
                password = cred[1]
                if username not in self.info["credentials"]:
                    self.info["credentials"][username] = {}
                # we might be losing passwords in case of multiple reset attempts on same username
                # or in case another collector already filled in a password for this user
                self.info["credentials"][username]['password'] = password
            if len(azure_creds) != 0:
                self.info["Azure"] = {}
                self.info["Azure"]['usernames'] = [cred[0] for cred in azure_creds]
        except Exception:
            # If we failed to collect azure info, no reason to fail all the collection. Log and continue.
            LOG.error("Failed collecting Azure info.", exc_info=True)

    def get_aws_info(self):
        # noinspection PyBroadException
        try:
            self.info['aws'] = AwsCollector().get_aws_info()
        except Exception:
            # If we failed to collect aws info, no reason to fail all the collection. Log and continue.
            LOG.error("Failed collecting AWS info.", exc_info=True)

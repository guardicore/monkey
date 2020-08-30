import logging
import sys
from enum import IntEnum

import psutil

from common.data.system_info_collectors_names import AZURE_CRED_COLLECTOR
from infection_monkey.network.info import get_host_subnets
from infection_monkey.system_info.azure_cred_collector import AzureCollector
from infection_monkey.system_info.netstat_collector import NetstatCollector
from infection_monkey.system_info.system_info_collectors_handler import \
    SystemInfoCollectorsHandler

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
        # Collect all hardcoded
        self.get_network_info()
        self.get_azure_info()

        # Collect all plugins
        SystemInfoCollectorsHandler().execute_all_configured()

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
            if AZURE_CRED_COLLECTOR not in WormConfiguration.system_info_collector_classes:
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
                self.info["credentials"][username]['username'] = username
            if len(azure_creds) != 0:
                self.info["Azure"] = {}
                self.info["Azure"]['usernames'] = [cred[0] for cred in azure_creds]
        except Exception:
            # If we failed to collect azure info, no reason to fail all the collection. Log and continue.
            LOG.error("Failed collecting Azure info.", exc_info=True)

import logging
import sys
from enum import IntEnum

import psutil

from infection_monkey.network.info import get_host_subnets
from infection_monkey.system_info.system_info_collectors_handler import SystemInfoCollectorsHandler

logger = logging.getLogger(__name__)

# Linux doesn't have WindowsError
try:
    WindowsError
except NameError:
    # noinspection PyShadowingBuiltins
    WindowsError = psutil.AccessDenied


class OperatingSystem(IntEnum):
    Windows = 0
    Linux = 1


class SystemInfoCollector(object):
    """
    A class that checks the current operating system and calls system information collecting
    modules accordingly
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
        self.info = {"credentials": {}}

    def get_info(self):
        # Collect all hardcoded
        self.get_network_info()

        # Collect all plugins
        SystemInfoCollectorsHandler().execute_all_configured()

    def get_network_info(self):
        """
        Adds network information from the host to the system information.
        Currently updates with list of networks accessible from host
        containing host ip and the subnet range
        :return: None. Updates class information
        """
        logger.debug("Reading subnets")
        self.info["network_info"] = {"networks": get_host_subnets()}

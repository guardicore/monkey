import logging

import infection_monkey.config
from infection_monkey.system_info.mimikatz_collector import MimikatzCollector
from infection_monkey.system_info import InfoCollector

LOG = logging.getLogger(__name__)

__author__ = 'uri'


class WindowsInfoCollector(InfoCollector):
    """
    System information collecting module for Windows operating systems
    """

    def __init__(self):
        super(WindowsInfoCollector, self).__init__()
        self._config = infection_monkey.config.WormConfiguration

    def get_info(self):
        """
        Collect Windows system information
        Hostname, process list and network subnets
        Tries to read credential secrets using mimikatz
        :return: Dict of system information
        """
        LOG.debug("Running Windows collector")
        self.get_hostname()
        self.get_process_list()
        self.get_network_info()
        self.get_azure_info()
        self._get_mimikatz_info()

        return self.info

    def _get_mimikatz_info(self):
        if self._config.should_use_mimikatz:
            LOG.info("Using mimikatz")
            self.info["credentials"].update(MimikatzCollector().get_logon_info())
        else:
            LOG.info("Not using mimikatz")

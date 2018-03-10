import logging

from mimikatz_collector import MimikatzCollector
from . import InfoCollector

LOG = logging.getLogger(__name__)

__author__ = 'uri'


class WindowsInfoCollector(InfoCollector):
    """
    System information collecting module for Windows operating systems
    """

    def __init__(self):
        super(WindowsInfoCollector, self).__init__()

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
        mimikatz_collector = MimikatzCollector()
        self.info["credentials"] = mimikatz_collector.get_logon_info()
        return self.info

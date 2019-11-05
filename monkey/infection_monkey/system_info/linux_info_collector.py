import logging

from infection_monkey.system_info import InfoCollector
from infection_monkey.system_info.SSH_info_collector import SSHCollector

__author__ = 'uri'

LOG = logging.getLogger(__name__)


class LinuxInfoCollector(InfoCollector):
    """
    System information collecting module for Linux operating systems
    """

    def __init__(self):
        super(LinuxInfoCollector, self).__init__()

    def get_info(self):
        """
        Collect Linux system information
        Hostname, process list and network subnets
        :return: Dict of system information
        """
        LOG.debug("Running Linux collector")
        super(LinuxInfoCollector, self).get_info()
        self.info['ssh_info'] = SSHCollector.get_info()
        return self.info

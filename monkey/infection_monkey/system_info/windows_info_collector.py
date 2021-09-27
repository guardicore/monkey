import logging
import sys

from common.common_consts.system_info_collectors_names import MIMIKATZ_COLLECTOR
from infection_monkey.system_info.windows_cred_collector.mimikatz_cred_collector import (
    MimikatzCredentialCollector,
)

sys.coinit_flags = 0  # needed for proper destruction of the wmi python module
import infection_monkey.config  # noqa: E402
from infection_monkey.system_info import InfoCollector  # noqa: E402

logger = logging.getLogger(__name__)
logger.info("started windows info collector")


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
        logger.debug("Running Windows collector")
        super(WindowsInfoCollector, self).get_info()
        # TODO: Think about returning self.get_wmi_info()
        from infection_monkey.config import WormConfiguration

        if MIMIKATZ_COLLECTOR in WormConfiguration.system_info_collector_classes:
            self.get_mimikatz_info()

        return self.info

    def get_mimikatz_info(self):
        logger.info("Gathering mimikatz info")
        try:
            credentials = MimikatzCredentialCollector.get_creds()
            if credentials:
                if "credentials" in self.info:
                    self.info["credentials"].update(credentials)
                logger.info("Mimikatz info gathered successfully")
            else:
                logger.info("No mimikatz info was gathered")
        except Exception as e:
            logger.info(f"Mimikatz credential collector failed: {e}")

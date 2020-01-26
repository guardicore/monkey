import logging

from common.data.system_info_collectors_names import SCOUTSUITE_COLLECTOR
from infection_monkey.system_info.system_info_collector import SystemInfoCollector
from infection_monkey.system_info.collectors.scoutsuite.ScoutSuite.__main__ import run

logger = logging.getLogger(__name__)


class HostnameCollector(SystemInfoCollector):
    def __init__(self):
        super().__init__(name=SCOUTSUITE_COLLECTOR)

    def collect(self) -> dict:

        return {}

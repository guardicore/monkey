import logging
import socket

from common.data.system_info_collectors_names import HOSTNAME_COLLECTOR
from infection_monkey.system_info.system_info_collector import \
    SystemInfoCollector

logger = logging.getLogger(__name__)


class HostnameCollector(SystemInfoCollector):
    def __init__(self):
        super().__init__(name=HOSTNAME_COLLECTOR)

    def collect(self) -> dict:
        return {"hostname": socket.getfqdn()}

from abc import abstractmethod
from typing import Dict

from agentpluginapi import PingScanData, PortScanData

from . import FingerprintData


class IFingerprinter:
    @abstractmethod
    def get_host_fingerprint(
        self,
        host: str,
        ping_scan_data: PingScanData,
        port_scan_data: Dict[int, PortScanData],
        options: Dict,
    ) -> FingerprintData:
        """
        Attempts to gather detailed information about a host and its services
        :param str host: The domain name or IP address of a host
        :param PingScanData ping_scan_data: Data retrieved from the target host via ICMP
        :param Dict[int, PortScanData] port_scan_data: Data retrieved from the target host via a TCP
                                                       port scan
        :param Dict options: A dictionary containing options that modify the behavior of the
                             fingerprinter
        :return: Detailed information about the target host
        :rtype: FingerprintData
        """
        pass

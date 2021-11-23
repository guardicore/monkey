import logging

from infection_monkey.i_master import IMaster
from infection_monkey.i_puppet import IPuppet, PortScanData, PortStatus
from infection_monkey.model.host import VictimHost
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.telemetry.scan_telem import ScanTelem
from infection_monkey.telemetry.system_info_telem import SystemInfoTelem

logger = logging.getLogger()


class MockMaster(IMaster):
    def __init__(self, puppet: IPuppet, telemetry_messenger: ITelemetryMessenger):
        self._puppet = puppet
        self._telemetry_messenger = telemetry_messenger

    def start(self) -> None:
        self._run_sys_info_collectors()
        self._run_pbas()
        self._scan_victims()

    def _run_sys_info_collectors(self):
        system_info_telemetry = {}
        system_info_telemetry["ProcessListCollector"] = self._puppet.run_sys_info_collector(
            "ProcessListCollector"
        )
        self._telemetry_messenger.send_telemetry(
            SystemInfoTelem({"collectors": system_info_telemetry})
        )
        system_info = self._puppet.run_sys_info_collector("LinuxInfoCollector")
        self._telemetry_messenger.send_telemetry(SystemInfoTelem(system_info))

    def _run_pbas(self):
        self._puppet.run_pba("AccountDiscovery", {})
        self._puppet.run_pba("CommunicateAsBackdoorUser", {})

    def _scan_victims(self):
        # TODO: The telemetry must be malformed somehow, or something else is wrong. This causes the
        #       Island to raise an error when reports are viewed.
        ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
        ports = [22, 445, 3389, 8008]
        for ip in ips:
            h = VictimHost(ip)

            (response_received, os) = self._puppet.ping(ip)
            h.icmp = response_received
            if os is not None:
                h.os["type"] = os

            for p in ports:
                port_scan_data = self._puppet.scan_tcp_port(ip, p)
                if port_scan_data.status == PortStatus.OPEN:
                    h.services[port_scan_data.service] = {}
                    h.services[port_scan_data.service]["display_name"] = "unknown(TCP)"
                    h.services[port_scan_data.service]["port"] = port_scan_data.port
                    if port_scan_data.banner is not None:
                        h.services[port_scan_data.service]["banner"] = port_scan_data.banner

            self._telemetry_messenger.send_telemetry(ScanTelem(h))

    def terminate(self) -> None:
        logger.info("Terminating MockMaster")

    def cleanup(self) -> None:
        pass

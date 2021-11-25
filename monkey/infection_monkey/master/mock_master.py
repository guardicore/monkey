import logging

from infection_monkey.i_master import IMaster
from infection_monkey.i_puppet import IPuppet, PortStatus
from infection_monkey.model.host import VictimHost
from infection_monkey.telemetry.exploit_telem import ExploitTelem
from infection_monkey.telemetry.file_encryption_telem import FileEncryptionTelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.telemetry.scan_telem import ScanTelem
from infection_monkey.telemetry.system_info_telem import SystemInfoTelem

logger = logging.getLogger()


class MockMaster(IMaster):
    def __init__(self, puppet: IPuppet, telemetry_messenger: ITelemetryMessenger):
        self._puppet = puppet
        self._telemetry_messenger = telemetry_messenger
        self._hosts = {
            "10.0.0.1": VictimHost("10.0.0.1"),
            "10.0.0.2": VictimHost("10.0.0.2"),
            "10.0.0.3": VictimHost("10.0.0.3"),
            "10.0.0.4": VictimHost("10.0.0.4"),
        }

    def start(self) -> None:
        self._run_sys_info_collectors()
        self._run_pbas()
        self._scan_victims()
        self._fingerprint()
        self._exploit()
        self._run_payload()

    def _run_sys_info_collectors(self):
        logger.info("Running system info collectors")
        system_info_telemetry = {}
        system_info_telemetry["ProcessListCollector"] = self._puppet.run_sys_info_collector(
            "ProcessListCollector"
        )
        self._telemetry_messenger.send_telemetry(
            SystemInfoTelem({"collectors": system_info_telemetry})
        )
        system_info = self._puppet.run_sys_info_collector("LinuxInfoCollector")
        self._telemetry_messenger.send_telemetry(SystemInfoTelem(system_info))
        logger.info("Finished running system info collectors")

    def _run_pbas(self):
        logger.info("Running post breach actions")
        name = "AccountDiscovery"
        command, result = self._puppet.run_pba(name, {})
        self._telemetry_messenger.send_telemetry(PostBreachTelem(name, command, result))

        name = "CommunicateAsBackdoorUser"
        command, result = self._puppet.run_pba(name, {})
        self._telemetry_messenger.send_telemetry(PostBreachTelem(name, command, result))
        logger.info("Finished running post breach actions")

    def _scan_victims(self):
        logger.info("Scanning network for potential victims")
        ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
        ports = [22, 445, 3389, 8008]
        for ip in ips:
            h = self._hosts[ip]

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
        logger.info("Finished scanning network for potential victims")

    def _fingerprint(self):
        logger.info("Running fingerprinters on potential victims")
        machine_1 = self._hosts["10.0.0.1"]
        machine_3 = self._hosts["10.0.0.3"]

        self._puppet.fingerprint("SMBFinger", machine_1)
        self._telemetry_messenger.send_telemetry(ScanTelem(machine_1))

        self._puppet.fingerprint("SMBFinger", machine_3)
        self._telemetry_messenger.send_telemetry(ScanTelem(machine_3))

        self._puppet.fingerprint("HTTPFinger", machine_3)
        self._telemetry_messenger.send_telemetry(ScanTelem(machine_3))
        logger.info("Finished running fingerprinters on potential victims")

    def _exploit(self):
        logger.info("Exploiting victims")
        result, info, attempts = self._puppet.exploit_host(
            "PowerShellExploiter", "10.0.0.1", {}, None
        )
        logger.info(f"Attempts for exploiting {attempts}")
        self._telemetry_messenger.send_telemetry(
            ExploitTelem("PowerShellExploiter", self._hosts["10.0.0.1"], result, info, attempts)
        )

        result, info, attempts = self._puppet.exploit_host("SSHExploiter", "10.0.0.3", {}, None)
        logger.info(f"Attempts for exploiting {attempts}")
        self._telemetry_messenger.send_telemetry(
            ExploitTelem("SSHExploiter", self._hosts["10.0.0.3"], result, info, attempts)
        )
        logger.info("Finished exploiting victims")

    def _run_payload(self):
        logger.info("Running payloads")
        # TODO: modify what FileEncryptionTelem gets
        path, success, error = self._puppet.run_payload("RansomwarePayload", {}, None)
        self._telemetry_messenger.send_telemetry(FileEncryptionTelem(path, success, error))
        logger.info("Finished running payloads")

    def terminate(self) -> None:
        logger.info("Terminating MockMaster")

    def cleanup(self) -> None:
        pass

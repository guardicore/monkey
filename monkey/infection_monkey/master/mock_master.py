import logging

from infection_monkey.i_master import IMaster
from infection_monkey.i_puppet import IPuppet, PortStatus
from infection_monkey.model.host import VictimHost
from infection_monkey.telemetry.credentials_telem import CredentialsTelem
from infection_monkey.telemetry.exploit_telem import ExploitTelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.telemetry.scan_telem import ScanTelem

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

    def _run_credential_collectors(self):
        logger.info("Running credential collectors")

        windows_credentials = self._puppet.run_credential_collector("MimikatzCollector")
        if windows_credentials:
            self._telemetry_messenger.send_telemetry(CredentialsTelem(windows_credentials))

        ssh_credentials = self._puppet.run_sys_info_collector("SSHCollector")
        if ssh_credentials:
            self._telemetry_messenger.send_telemetry(CredentialsTelem(ssh_credentials))

        logger.info("Finished running credential collectors")

    def _run_pbas(self):

        # TODO: Create monkey_dir and revise setup in monkey.py

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

            ping_scan_data = self._puppet.ping(ip, 1)
            h.icmp = ping_scan_data.response_received
            if ping_scan_data.os is not None:
                h.os["type"] = ping_scan_data.os

            ports_scan_data = self._puppet.scan_tcp_ports(ip, ports)

            for psd in ports_scan_data.values():
                logger.debug(f"The port {psd.port} is {psd.status}")
                if psd.status == PortStatus.OPEN:
                    h.services[psd.service] = {}
                    h.services[psd.service]["display_name"] = "unknown(TCP)"
                    h.services[psd.service]["port"] = psd.port
                    if psd.banner is not None:
                        h.services[psd.service]["banner"] = psd.banner

            self._telemetry_messenger.send_telemetry(ScanTelem(h))
        logger.info("Finished scanning network for potential victims")

    def _fingerprint(self):
        logger.info("Running fingerprinters on potential victims")
        machine_1 = self._hosts["10.0.0.1"]
        machine_3 = self._hosts["10.0.0.3"]

        self._puppet.fingerprint("SMBFinger", machine_1, None, None, None)
        self._telemetry_messenger.send_telemetry(ScanTelem(machine_1))

        self._puppet.fingerprint("SMBFinger", machine_3, None, None, None)
        self._telemetry_messenger.send_telemetry(ScanTelem(machine_3))

        self._puppet.fingerprint("HTTPFinger", machine_3, None, None, None)
        self._telemetry_messenger.send_telemetry(ScanTelem(machine_3))
        logger.info("Finished running fingerprinters on potential victims")

    def _exploit(self):
        logger.info("Exploiting victims")
        result, info, attempts, error_message = self._puppet.exploit_host(
            "PowerShellExploiter", "10.0.0.1", {}, None
        )
        logger.info(f"Attempts for exploiting {attempts}")
        self._telemetry_messenger.send_telemetry(
            ExploitTelem("PowerShellExploiter", self._hosts["10.0.0.1"], result, info, attempts)
        )

        result, info, attempts, error_message = self._puppet.exploit_host(
            "SSHExploiter", "10.0.0.3", {}, None
        )
        logger.info(f"Attempts for exploiting {attempts}")
        self._telemetry_messenger.send_telemetry(
            ExploitTelem("SSHExploiter", self._hosts["10.0.0.3"], result, info, attempts)
        )
        logger.info("Finished exploiting victims")

    def _run_payload(self):
        logger.info("Running payloads")
        self._puppet.run_payload("RansomwarePayload", {}, None)
        logger.info("Finished running payloads")

    def terminate(self, block: bool = False) -> None:
        logger.info("Terminating MockMaster")

    def cleanup(self) -> None:
        # TODO: Cleanup monkey_dir and send telemetry
        pass

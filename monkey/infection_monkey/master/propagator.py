import logging
from queue import Queue
from threading import Event, Thread
from typing import Dict

from infection_monkey.i_puppet import FingerprintData, PingScanData, PortScanData, PortStatus
from infection_monkey.model.host import VictimHost
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.telemetry.scan_telem import ScanTelem

from . import IPScanner, IPScanResults
from .threading_utils import create_daemon_thread

logger = logging.getLogger()


class Propagator:
    def __init__(self, telemetry_messenger: ITelemetryMessenger, ip_scanner: IPScanner):
        self._telemetry_messenger = telemetry_messenger
        self._ip_scanner = ip_scanner
        self._hosts_to_exploit = None

    def propagate(self, propagation_config: Dict, stop: Event):
        logger.info("Attempting to propagate")

        self._hosts_to_exploit = Queue()

        scan_thread = create_daemon_thread(
            target=self._scan_network, args=(propagation_config, stop)
        )
        exploit_thread = create_daemon_thread(
            target=self._exploit_targets, args=(scan_thread, stop)
        )

        scan_thread.start()
        exploit_thread.start()

        scan_thread.join()
        exploit_thread.join()

        logger.info("Finished attempting to propagate")

    def _scan_network(self, propagation_config: Dict, stop: Event):
        logger.info("Starting network scan")

        # TODO: Generate list of IPs to scan from propagation targets config
        ips_to_scan = propagation_config["targets"]["subnet_scan_list"]

        scan_config = propagation_config["network_scan"]
        self._ip_scanner.scan(ips_to_scan, scan_config, self._process_scan_results, stop)

        logger.info("Finished network scan")

    def _process_scan_results(self, ip: str, scan_results: IPScanResults):
        victim_host = VictimHost(ip)

        Propagator._process_ping_scan_results(victim_host, scan_results.ping_scan_data)
        has_open_port = Propagator._process_tcp_scan_results(
            victim_host, scan_results.port_scan_data
        )
        Propagator._process_fingerprinter_results(victim_host, scan_results.fingerprint_data)

        if has_open_port:
            self._hosts_to_exploit.put(victim_host)

        self._telemetry_messenger.send_telemetry(ScanTelem(victim_host))

    @staticmethod
    def _process_ping_scan_results(victim_host: VictimHost, ping_scan_data: PingScanData):
        victim_host.icmp = ping_scan_data.response_received
        if ping_scan_data.os is not None:
            victim_host.os["type"] = ping_scan_data.os

    @staticmethod
    def _process_tcp_scan_results(victim_host: VictimHost, port_scan_data: PortScanData) -> bool:
        has_open_port = False

        for psd in port_scan_data.values():
            if psd.status == PortStatus.OPEN:
                has_open_port = True

                victim_host.services[psd.service] = {}
                victim_host.services[psd.service]["display_name"] = "unknown(TCP)"
                victim_host.services[psd.service]["port"] = psd.port
                if psd.banner is not None:
                    victim_host.services[psd.service]["banner"] = psd.banner

        return has_open_port

    @staticmethod
    def _process_fingerprinter_results(victim_host: VictimHost, fingerprint_data: FingerprintData):
        for fd in fingerprint_data.values():
            # TODO: This logic preserves the existing behavior prior to introducing IMaster and
            #       IPuppet, but it is possibly flawed. Different fingerprinters may detect
            #       different os types or versions, and this logic isn't sufficient to handle those
            #       conflicts. Reevaluate this logic when we overhaul our scanners/fingerprinters.
            if fd.os_type is not None:
                victim_host.os["type"] = fd.os_type

            if ("version" not in victim_host.os) and (fd.os_version is not None):
                victim_host.os["version"] = fd.os_version

            for service, details in fd.services.items():
                victim_host.services.setdefault(service, {}).update(details)

    def _exploit_targets(self, scan_thread: Thread, stop: Event):
        pass

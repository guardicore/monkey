import logging
from queue import Queue
from threading import Event
from typing import List, Sequence

from common.agent_configuration import (
    ExploitationConfiguration,
    NetworkScanConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
)
from infection_monkey.i_puppet import (
    ExploiterResultData,
    FingerprintData,
    PingScanData,
    PortScanData,
    PortStatus,
)
from infection_monkey.model import VictimHost, VictimHostFactory
from infection_monkey.network import NetworkAddress, NetworkInterface
from infection_monkey.network_scanning.scan_target_generator import compile_scan_target_list
from infection_monkey.telemetry.exploit_telem import ExploitTelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.telemetry.scan_telem import ScanTelem
from infection_monkey.utils.threading import create_daemon_thread

from . import Exploiter, IPScanner, IPScanResults

logger = logging.getLogger()


class Propagator:
    def __init__(
        self,
        telemetry_messenger: ITelemetryMessenger,
        ip_scanner: IPScanner,
        exploiter: Exploiter,
        victim_host_factory: VictimHostFactory,
        local_network_interfaces: List[NetworkInterface],
    ):
        self._telemetry_messenger = telemetry_messenger
        self._ip_scanner = ip_scanner
        self._exploiter = exploiter
        self._victim_host_factory = victim_host_factory
        self._local_network_interfaces = local_network_interfaces
        self._hosts_to_exploit = None

    def propagate(
        self, propagation_config: PropagationConfiguration, current_depth: int, stop: Event
    ):
        logger.info("Attempting to propagate")

        network_scan_completed = Event()
        self._hosts_to_exploit = Queue()

        network_scan = self._add_http_ports_to_fingerprinters(
            propagation_config.network_scan, propagation_config.exploitation.options.http_ports
        )

        scan_thread = create_daemon_thread(
            target=self._scan_network,
            name="PropagatorScanThread",
            args=(network_scan, stop),
        )
        exploit_thread = create_daemon_thread(
            target=self._exploit_hosts,
            name="PropagatorExploitThread",
            args=(propagation_config.exploitation, current_depth, network_scan_completed, stop),
        )

        scan_thread.start()
        exploit_thread.start()

        scan_thread.join()
        network_scan_completed.set()

        exploit_thread.join()

        logger.info("Finished attempting to propagate")

    @staticmethod
    def _add_http_ports_to_fingerprinters(
        network_scan: NetworkScanConfiguration, http_ports: Sequence[int]
    ) -> NetworkScanConfiguration:
        # This is a hack to add http_ports to the options of fingerprinters
        # It will be reworked. See https://github.com/guardicore/monkey/issues/2136
        modified_fingerprinters = [*network_scan.fingerprinters]
        for i, fingerprinter in enumerate(modified_fingerprinters):
            if fingerprinter.name != "http":
                continue

            modified_options = fingerprinter.options.copy()
            modified_options["http_ports"] = list(http_ports)
            modified_fingerprinters[i] = fingerprinter.copy(update={"options": modified_options})

        return network_scan.copy(update={"fingerprinters": modified_fingerprinters})

    def _scan_network(self, scan_config: NetworkScanConfiguration, stop: Event):
        logger.info("Starting network scan")

        addresses_to_scan = self._compile_scan_target_list(scan_config.targets)
        self._ip_scanner.scan(addresses_to_scan, scan_config, self._process_scan_results, stop)

        logger.info("Finished network scan")

    def _compile_scan_target_list(
        self, target_config: ScanTargetConfiguration
    ) -> List[NetworkAddress]:
        ranges_to_scan = target_config.subnets
        inaccessible_subnets = target_config.inaccessible_subnets
        blocklisted_ips = target_config.blocked_ips
        enable_local_network_scan = target_config.local_network_scan

        return compile_scan_target_list(
            self._local_network_interfaces,
            ranges_to_scan,
            inaccessible_subnets,
            blocklisted_ips,
            enable_local_network_scan,
        )

    def _process_scan_results(self, address: NetworkAddress, scan_results: IPScanResults):
        victim_host = self._victim_host_factory.build_victim_host(address)

        Propagator._process_ping_scan_results(victim_host, scan_results.ping_scan_data)
        Propagator._process_tcp_scan_results(victim_host, scan_results.port_scan_data)
        Propagator._process_fingerprinter_results(victim_host, scan_results.fingerprint_data)

        if IPScanner.port_scan_found_open_port(scan_results.port_scan_data):
            self._hosts_to_exploit.put(victim_host)

        self._telemetry_messenger.send_telemetry(ScanTelem(victim_host))

    @staticmethod
    def _process_ping_scan_results(victim_host: VictimHost, ping_scan_data: PingScanData):
        victim_host.icmp = ping_scan_data.response_received
        if ping_scan_data.os is not None:
            victim_host.os["type"] = ping_scan_data.os

    @staticmethod
    def _process_tcp_scan_results(victim_host: VictimHost, port_scan_data: PortScanData):
        for psd in filter(lambda psd: psd.status == PortStatus.OPEN, port_scan_data.values()):
            victim_host.services[psd.service] = {}
            victim_host.services[psd.service]["display_name"] = "unknown(TCP)"
            victim_host.services[psd.service]["port"] = psd.port
            if psd.banner is not None:
                victim_host.services[psd.service]["banner"] = psd.banner

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

    def _exploit_hosts(
        self,
        exploitation_config: ExploitationConfiguration,
        current_depth: int,
        network_scan_completed: Event,
        stop: Event,
    ):
        logger.info("Exploiting victims")

        self._exploiter.exploit_hosts(
            exploitation_config,
            self._hosts_to_exploit,
            current_depth,
            self._process_exploit_attempts,
            network_scan_completed,
            stop,
        )

        logger.info("Finished exploiting victims")

    def _process_exploit_attempts(
        self, exploiter_name: str, host: VictimHost, result: ExploiterResultData
    ):
        if result.propagation_success:
            logger.info(f"Successfully propagated to {host} using {exploiter_name}")
        elif result.exploitation_success:
            logger.info(
                f"Successfully exploited (but did not propagate to) {host} using {exploiter_name}"
            )
        else:
            logger.info(
                f"Failed to exploit or propagate to {host} using {exploiter_name}: "
                f"{result.error_message}"
            )

        self._telemetry_messenger.send_telemetry(ExploitTelem(exploiter_name, host, result))

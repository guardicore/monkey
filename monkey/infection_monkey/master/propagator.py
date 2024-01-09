import logging
import threading
from ipaddress import IPv4Address, IPv4Interface
from queue import Queue
from typing import List, Mapping, MutableMapping, Sequence

from monkeytoolbox import create_daemon_thread
from monkeytypes import (
    DiscoveredService,
    Event,
    NetworkPort,
    NetworkProtocol,
    NetworkService,
    PortStatus,
)

from common.agent_configuration import (
    ExploitationConfiguration,
    NetworkScanConfiguration,
    PropagationConfiguration,
    ScanTargetConfiguration,
)
from infection_monkey.i_puppet import (
    ExploiterResult,
    FingerprintData,
    PingScanData,
    PortScanData,
    TargetHost,
)
from infection_monkey.network import NetworkAddress
from infection_monkey.network_scanning.scan_target_generator import compile_scan_target_list

from . import Exploiter, IPScanner, IPScanResults
from .ip_scan_results import FingerprinterName

logger = logging.getLogger()


class Propagator:
    def __init__(
        self,
        ip_scanner: IPScanner,
        exploiter: Exploiter,
        local_network_interfaces: List[IPv4Interface],
    ):
        self._ip_scanner = ip_scanner
        self._exploiter = exploiter
        self._local_network_interfaces = local_network_interfaces
        self._hosts_to_exploit: Queue = Queue()

    def propagate(
        self,
        propagation_config: PropagationConfiguration,
        current_depth: int,
        servers: Sequence[str],
        stop: Event,
    ):
        logger.info("Attempting to propagate")

        network_scan_completed = threading.Event()
        self._hosts_to_exploit = Queue()

        scan_thread = create_daemon_thread(
            target=self._scan_network,
            name="PropagatorScanThread",
            args=(propagation_config.network_scan, stop),
        )
        exploit_thread = create_daemon_thread(
            target=self._exploit_hosts,
            name="PropagatorExploitThread",
            args=(
                propagation_config.exploitation,
                current_depth,
                servers,
                network_scan_completed,
                stop,
            ),
        )

        scan_thread.start()
        exploit_thread.start()

        scan_thread.join()
        network_scan_completed.set()

        exploit_thread.join()

        logger.info("Finished attempting to propagate")

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
        scan_my_networks = target_config.scan_my_networks

        return compile_scan_target_list(
            self._local_network_interfaces,
            ranges_to_scan,
            inaccessible_subnets,
            blocklisted_ips,
            scan_my_networks,
        )

    def _process_scan_results(self, address: NetworkAddress, scan_results: IPScanResults):
        target_host = TargetHost(ip=IPv4Address(address.ip))

        Propagator._process_ping_scan_results(target_host, scan_results.ping_scan_data)
        Propagator._process_tcp_scan_results(target_host, scan_results.port_scan_data)
        Propagator._process_fingerprinter_results(target_host, scan_results.fingerprint_data)

        if IPScanner.port_scan_found_open_port(scan_results.port_scan_data):
            self._hosts_to_exploit.put(target_host)

    @staticmethod
    def _process_ping_scan_results(target_host: TargetHost, ping_scan_data: PingScanData):
        target_host.icmp = ping_scan_data.response_received
        if ping_scan_data.os is not None:
            target_host.operating_system = ping_scan_data.os

    @staticmethod
    def _process_tcp_scan_results(
        target_host: TargetHost, port_scan_data: Mapping[NetworkPort, PortScanData]
    ):
        for psd in port_scan_data.values():
            if psd.port in target_host.ports_status.tcp_ports:
                logger.warning("Unexpected TCP scan data is being overwritten.")

            target_host.ports_status.tcp_ports[psd.port] = psd

    @staticmethod
    def _process_fingerprinter_results(
        target_host: TargetHost, fingerprint_data: Mapping[FingerprinterName, FingerprintData]
    ):
        for fd in fingerprint_data.values():
            # TODO: This logic preserves the existing behavior prior to introducing IMaster and
            #       IPuppet, but it is possibly flawed. Different fingerprinters may detect
            #       different os types or versions, and this logic isn't sufficient to handle those
            #       conflicts. Reevaluate this logic when we overhaul our scanners/fingerprinters.
            if fd.os_type is not None:
                target_host.operating_system = fd.os_type

            for discovered_service in fd.services:
                if discovered_service.protocol == NetworkProtocol.TCP:
                    Propagator._update_port_data(
                        target_host.ports_status.tcp_ports, discovered_service
                    )

                elif discovered_service.protocol == NetworkProtocol.UDP:
                    Propagator._update_port_data(
                        target_host.ports_status.udp_ports, discovered_service
                    )

    @staticmethod
    def _update_port_data(
        ports: MutableMapping[NetworkPort, PortScanData], discovered_service: DiscoveredService
    ):
        protocol = discovered_service.protocol
        port = discovered_service.port
        service = discovered_service.service
        banner = None

        if port in ports:
            existing_psd = ports[port]

            if service == NetworkService.UNKNOWN:
                service = existing_psd.service
            banner = existing_psd.banner

        ports[port] = PortScanData(
            port=port,
            status=PortStatus.OPEN,
            protocol=protocol,
            service=service,
            banner=banner,
        )

    def _exploit_hosts(
        self,
        exploitation_config: ExploitationConfiguration,
        current_depth: int,
        servers: Sequence[str],
        network_scan_completed: threading.Event,
        stop: Event,
    ):
        logger.info("Exploiting victims")

        self._exploiter.exploit_hosts(
            exploitation_config,
            self._hosts_to_exploit,
            current_depth,
            servers,
            self._process_exploit_attempts,
            network_scan_completed,
            stop,
        )

        logger.info("Finished exploiting victims")

    def _process_exploit_attempts(
        self, exploiter_name: str, host: TargetHost, result: ExploiterResult
    ):
        if result.propagation_success:
            logger.info(f"Successfully propagated to {host.ip} using {exploiter_name}")
        elif result.exploitation_success:
            logger.info(
                f"Successfully exploited (but did not propagate to) {host.ip} using "
                f"{exploiter_name}"
            )
        else:
            logger.info(
                f"Failed to exploit or propagate to {host.ip} using {exploiter_name}: "
                f"{result.error_message}"
            )

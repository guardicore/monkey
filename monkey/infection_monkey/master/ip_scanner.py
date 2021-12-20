import logging
import queue
import threading
from queue import Queue
from threading import Event
from typing import Callable, Dict, List

from infection_monkey.i_puppet import (
    FingerprintData,
    IPuppet,
    PingScanData,
    PortScanData,
    PortStatus,
)
from infection_monkey.network import NetworkAddress

from . import IPScanResults
from .threading_utils import run_worker_threads

logger = logging.getLogger()

Callback = Callable[[NetworkAddress, IPScanResults], None]


class IPScanner:
    def __init__(self, puppet: IPuppet, num_workers: int):
        self._puppet = puppet
        self._num_workers = num_workers

    def scan(
        self,
        addresses_to_scan: List[NetworkAddress],
        options: Dict,
        results_callback: Callback,
        stop: Event,
    ):
        # Pre-fill a Queue with all IPs to scan so that threads know they can safely exit when the
        # queue is empty.
        addresses = Queue()
        for address in addresses_to_scan:
            addresses.put(address)

        scan_ips_args = (addresses, options, results_callback, stop)
        run_worker_threads(
            target=self._scan_addresses, args=scan_ips_args, num_workers=self._num_workers
        )

    def _scan_addresses(
        self, addresses: Queue, options: Dict, results_callback: Callback, stop: Event
    ):
        logger.debug(f"Starting scan thread -- Thread ID: {threading.get_ident()}")

        try:
            while not stop.is_set():
                address = addresses.get_nowait()
                ip = address.ip
                logger.info(f"Scanning {ip}")

                icmp_timeout = options["icmp"]["timeout_ms"] / 1000
                ping_scan_data = self._puppet.ping(ip, icmp_timeout)

                tcp_timeout = options["tcp"]["timeout_ms"] / 1000
                tcp_ports = options["tcp"]["ports"]
                port_scan_data = self._scan_tcp_ports(ip, tcp_ports, tcp_timeout, stop)

                fingerprint_data = {}
                if IPScanner.port_scan_found_open_port(port_scan_data):
                    fingerprinters = options["fingerprinters"]
                    fingerprint_data = self._run_fingerprinters(
                        ip, fingerprinters, ping_scan_data, port_scan_data, stop
                    )

                scan_results = IPScanResults(ping_scan_data, port_scan_data, fingerprint_data)
                results_callback(address, scan_results)

            logger.debug(
                f"Detected the stop signal, scanning thread {threading.get_ident()} exiting"
            )

        except queue.Empty:
            logger.debug(
                f"ips_to_scan queue is empty, scanning thread {threading.get_ident()} exiting"
            )

    def _scan_tcp_ports(
        self, ip: str, ports: List[int], timeout: float, stop: Event
    ) -> Dict[int, PortScanData]:
        port_scan_data = {}

        for p in ports:
            if stop.is_set():
                break

            port_scan_data[p] = self._puppet.scan_tcp_port(ip, p, timeout)

        return port_scan_data

    @staticmethod
    def port_scan_found_open_port(port_scan_data: Dict[int, PortScanData]):
        return any(psd.status == PortStatus.OPEN for psd in port_scan_data.values())

    def _run_fingerprinters(
        self,
        ip: str,
        fingerprinters: List[str],
        ping_scan_data: PingScanData,
        port_scan_data: Dict[int, PortScanData],
        stop: Event,
    ) -> Dict[str, FingerprintData]:
        fingerprint_data = {}

        for f in fingerprinters:
            if stop.is_set():
                break

            fingerprint_data[f] = self._puppet.fingerprint(f, ip, ping_scan_data, port_scan_data)

        return fingerprint_data

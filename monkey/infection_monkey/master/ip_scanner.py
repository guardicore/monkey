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
from infection_monkey.utils.threading import interruptable_iter, run_worker_threads

from . import IPScanResults

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
        icmp_timeout = options["icmp"]["timeout_ms"] / 1000
        tcp_timeout = options["tcp"]["timeout_ms"] / 1000
        tcp_ports = options["tcp"]["ports"]

        try:
            while not stop.is_set():
                address = addresses.get_nowait()
                logger.info(f"Scanning {address.ip}")

                ping_scan_data = self._puppet.ping(address.ip, icmp_timeout)
                port_scan_data = self._puppet.scan_tcp_ports(address.ip, tcp_ports, tcp_timeout)

                fingerprint_data = {}
                if IPScanner.port_scan_found_open_port(port_scan_data):
                    fingerprinters = options["fingerprinters"]
                    fingerprint_data = self._run_fingerprinters(
                        address.ip, fingerprinters, ping_scan_data, port_scan_data, stop
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

        for f in interruptable_iter(fingerprinters, stop):
            fingerprint_data[f] = self._puppet.fingerprint(f, ip, ping_scan_data, port_scan_data)

        return fingerprint_data

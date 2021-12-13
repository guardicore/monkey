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

from .threading_utils import create_daemon_thread

logger = logging.getLogger()

IP = str
Port = int
FingerprinterName = str
Callback = Callable[
    [IP, PingScanData, Dict[Port, PortScanData], Dict[FingerprinterName, FingerprintData]], None
]


class IPScanner:
    def __init__(self, puppet: IPuppet, num_workers: int):
        self._puppet = puppet
        self._num_workers = num_workers

    def scan(self, ips_to_scan: List[str], options: Dict, results_callback: Callback, stop: Event):
        # Pre-fill a Queue with all IPs to scan so that threads know they can safely exit when the
        # queue is empty.
        ips = Queue()
        for ip in ips_to_scan:
            ips.put(ip)

        scan_ips_args = (ips, options, results_callback, stop)
        scan_threads = []
        for i in range(0, self._num_workers):
            t = create_daemon_thread(target=self._scan_ips, args=scan_ips_args)
            t.start()
            scan_threads.append(t)

        for t in scan_threads:
            t.join()

    def _scan_ips(self, ips: Queue, options: Dict, results_callback: Callback, stop: Event):
        logger.debug(f"Starting scan thread -- Thread ID: {threading.get_ident()}")

        try:
            while not stop.is_set():
                ip = ips.get_nowait()
                logger.info(f"Scanning {ip}")

                icmp_timeout = options["icmp"]["timeout_ms"] / 1000
                ping_scan_data = self._puppet.ping(ip, icmp_timeout)

                tcp_timeout = options["tcp"]["timeout_ms"] / 1000
                tcp_ports = options["tcp"]["ports"]
                port_scan_data = self._scan_tcp_ports(ip, tcp_ports, tcp_timeout, stop)

                fingerprint_data = {}
                if IPScanner._found_open_port(port_scan_data):
                    fingerprinters = options["fingerprinters"]
                    fingerprint_data = self._run_fingerprinters(ip, fingerprinters, stop)

                results_callback(ip, ping_scan_data, port_scan_data, fingerprint_data)

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
    def _found_open_port(port_scan_data: Dict[int, PortScanData]):
        for psd in port_scan_data.values():
            if psd.status == PortStatus.OPEN:
                return True

        return False

    def _run_fingerprinters(self, ip: str, fingerprinters: List[str], stop: Event):
        fingerprint_data = {}

        for f in fingerprinters:
            if stop.is_set():
                break

            fingerprint_data[f] = self._puppet.fingerprint(f, ip)

        return fingerprint_data

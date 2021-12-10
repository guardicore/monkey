import logging
import queue
import threading
from queue import Queue
from threading import Event
from typing import Callable, Dict, List

from infection_monkey.i_puppet import IPuppet, PortStatus
from infection_monkey.model.host import VictimHost

from .threading_utils import create_daemon_thread

logger = logging.getLogger()

Callback = Callable[[VictimHost], None]


class IPScanner:
    def __init__(self, puppet: IPuppet, num_workers: int):
        self._puppet = puppet
        self._num_workers = num_workers

    def scan(
        self,
        ips: List[str],
        icmp_config: Dict,
        tcp_config: Dict,
        report_results_callback: Callback,
        stop: Event,
    ):
        # Pre-fill a Queue with all IPs so that threads can safely exit when the queue is empty.
        ips_to_scan = Queue()
        for ip in ips:
            ips_to_scan.put(ip)

        scan_ips_args = (
            ips_to_scan,
            icmp_config,
            tcp_config,
            report_results_callback,
            stop,
        )
        scan_threads = []
        for i in range(0, self._num_workers):
            t = create_daemon_thread(target=self._scan_ips, args=scan_ips_args)
            t.start()
            scan_threads.append(t)

        for t in scan_threads:
            t.join()

    def _scan_ips(
        self,
        ips_to_scan: Queue,
        icmp_config: Dict,
        tcp_config: Dict,
        report_results_callback: Callback,
        stop: Event,
    ):
        logger.debug(f"Starting scan thread -- Thread ID: {threading.get_ident()}")

        try:
            while not stop.is_set():
                ip = ips_to_scan.get_nowait()
                logger.info(f"Scanning {ip}")

                victim_host = VictimHost(ip)

                self._ping_ip(ip, victim_host, icmp_config)
                self._scan_tcp_ports(ip, victim_host, tcp_config, stop)

                report_results_callback(victim_host)

        except queue.Empty:
            logger.debug(
                f"ips_to_scan queue is empty, scanning thread {threading.get_ident()} exiting"
            )
            return

        logger.debug(f"Detected the stop signal, scanning thread {threading.get_ident()} exiting")

    def _ping_ip(self, ip: str, victim_host: VictimHost, options: Dict):
        (response_received, os) = self._puppet.ping(ip, options)

        victim_host.icmp = response_received
        if os is not None:
            victim_host.os["type"] = os

    def _scan_tcp_ports(self, ip: str, victim_host: VictimHost, options: Dict, stop: Event):
        for p in options["ports"]:
            if stop.is_set():
                break

            port_scan_data = self._puppet.scan_tcp_port(ip, p, options["timeout_ms"])
            if port_scan_data.status == PortStatus.OPEN:
                victim_host.services[port_scan_data.service] = {}
                victim_host.services[port_scan_data.service]["display_name"] = "unknown(TCP)"
                victim_host.services[port_scan_data.service]["port"] = port_scan_data.port
                if port_scan_data.banner is not None:
                    victim_host.services[port_scan_data.service]["banner"] = port_scan_data.banner

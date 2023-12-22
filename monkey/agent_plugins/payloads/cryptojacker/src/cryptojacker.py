import logging

from egg_timer import EggTimer
from monkeytypes import Event

from .bitcoin_mining_network_traffic_simulator import BitcoinMiningNetworkTrafficSimulator
from .cpu_utilizer import CPUUtilizer
from .cryptojacker_options import CryptojackerOptions
from .memory_utilizer import MemoryUtilizer

logger = logging.getLogger(__name__)

COMPONENT_STOP_TIMEOUT = 30  # seconds
CHECK_DURATION_TIMER_INTERVAL = 5  # seconds


class Cryptojacker:
    def __init__(
        self,
        options: CryptojackerOptions,
        cpu_utilizer: CPUUtilizer,
        memory_utilizer: MemoryUtilizer,
        bitcoin_mining_network_traffic_simulator: BitcoinMiningNetworkTrafficSimulator,
    ):
        self._options = options
        self._cpu_utilizer = cpu_utilizer
        self._memory_utilizer = memory_utilizer
        self._bitcoin_mining_network_traffic_simulator = bitcoin_mining_network_traffic_simulator

    def run(self, interrupt: Event):
        self._start()

        timer = EggTimer()
        timer.set(self._options.duration)
        while not timer.is_expired() and not interrupt.is_set():
            interrupt.wait(CHECK_DURATION_TIMER_INTERVAL)

        self._stop()

    def _start(self):
        logger.info("Starting the cryptojacker payload")
        if self._options.cpu_utilization > 0:
            self._cpu_utilizer.start()

        self._memory_utilizer.start()

        if self._options.simulate_bitcoin_mining_network_traffic:
            self._bitcoin_mining_network_traffic_simulator.start()

    def _stop(self):
        logger.info("Stopping the cryptojacker payload")
        if self._options.cpu_utilization > 0:
            self._cpu_utilizer.stop(timeout=COMPONENT_STOP_TIMEOUT)

        self._memory_utilizer.stop(timeout=COMPONENT_STOP_TIMEOUT)

        if self._options.simulate_bitcoin_mining_network_traffic:
            self._bitcoin_mining_network_traffic_simulator.stop(timeout=COMPONENT_STOP_TIMEOUT)

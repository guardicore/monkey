import logging
from typing import Optional, Tuple

from infection_monkey.model import TargetHost
from infection_monkey.network import NetworkAddress
from infection_monkey.network.tools import get_interface_to_target

logger = logging.getLogger(__name__)


class TargetHostFactory:
    def __init__(
        self,
        island_ip: Optional[str],
        island_port: Optional[str],
        on_island: bool,
    ):
        self.island_ip = island_ip
        self.island_port = island_port
        self.on_island = on_island

    def build_target_host(self, network_address: NetworkAddress) -> TargetHost:
        target_host = TargetHost(network_address.ip)

        if self.island_ip:
            ip, port = self._choose_island_address(target_host.ip_addr)

        logger.debug(f"Default server for {target_host} set to {target_host.default_server}")

        return target_host

    def _choose_island_address(self, victim_ip: str) -> Tuple[Optional[str], Optional[str]]:
        # Victims need to connect back to the interface they can reach
        # On island, choose the right interface to pass to children monkeys
        if self.on_island:
            default_server_port = self.island_port if self.island_port else None
            interface = get_interface_to_target(victim_ip)

            return interface, default_server_port
        else:
            return self.island_ip, self.island_port

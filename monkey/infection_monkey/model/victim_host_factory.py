import logging
from typing import Optional

from infection_monkey.model import VictimHost
from infection_monkey.network import NetworkAddress
from infection_monkey.network.tools import get_interface_to_target
from infection_monkey.tunnel import MonkeyTunnel

logger = logging.getLogger(__name__)


class VictimHostFactory:
    def __init__(
        self,
        tunnel: Optional[MonkeyTunnel],
        default_server: Optional[str],
        default_port: Optional[str],
        on_island: bool,
    ):
        self.tunnel = tunnel
        self.default_server = default_server
        self.default_port = default_port
        self.on_island = on_island

    def build_victim_host(self, network_address: NetworkAddress) -> VictimHost:
        victim_host = VictimHost(network_address.ip, network_address.domain)

        if self.tunnel:
            victim_host.default_tunnel = self.tunnel.get_tunnel_for_ip(victim_host.ip_addr)
        if self.default_server:
            if self.on_island:
                victim_host.set_default_server(
                    get_interface_to_target(victim_host.ip_addr)
                    + (":" + self.default_port if self.default_port else "")
                )
            else:
                victim_host.set_default_server(self.default_server)
        logger.debug(
            f"Default server for machine: {victim_host} set to {victim_host.default_server}"
        )
        logger.debug(
            f"Default tunnel for machine: {victim_host} set to {victim_host.default_tunnel}"
        )

        return victim_host

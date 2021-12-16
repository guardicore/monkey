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
        domain = network_address.domain or ""
        victim_host = VictimHost(network_address.ip, domain)

        if self.tunnel:
            victim_host.default_tunnel = self.tunnel.get_tunnel_for_ip(victim_host.ip_addr)

        if self.default_server:
            victim_host.set_default_server(self._get_formatted_default_server(victim_host.ip_addr))

        logger.debug(f"Default tunnel for {victim_host} set to {victim_host.default_tunnel}")
        logger.debug(f"Default server for {victim_host} set to {victim_host.default_server}")

        return victim_host

    def _get_formatted_default_server(self, ip: str):
        if self.on_island:
            default_server_port = f":{self.default_port}" if self.default_port else ""
            interface = get_interface_to_target(ip)

            return f"{interface}{default_server_port}"
        else:
            return self.default_server

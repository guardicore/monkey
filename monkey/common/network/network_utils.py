from ipaddress import IPv4Address
from typing import List, Optional, Sequence

import psutil


def get_connections(
    ports: Optional[Sequence[int]] = None,
    ip_addresses: Optional[Sequence[IPv4Address]] = None,
) -> List[psutil._common.sconn]:
    connections = psutil.net_connections()
    if ports:
        connections = [connection for connection in connections if connection.laddr.port in ports]
    if ip_addresses:
        ip_addresses_ = list(map(str, ip_addresses))
        connections = [
            connection for connection in connections if connection.laddr.ip in ip_addresses_
        ]
    return connections

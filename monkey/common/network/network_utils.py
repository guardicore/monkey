from typing import Optional, Tuple


def address_to_ip_port(address: str) -> Tuple[str, Optional[str]]:
    if ":" in address:
        ip, port = address.split(":")
        return ip, port or None
    else:
        return address, None

import re
from typing import Optional, Tuple
from urllib.parse import urlparse


def remove_port(url):
    parsed = urlparse(url)
    with_port = f"{parsed.scheme}://{parsed.netloc}"
    without_port = re.sub(":[0-9]+(?=$|/)", "", with_port)
    return without_port


def address_to_ip_port(address: str) -> Tuple[str, Optional[str]]:
    if ":" in address:
        ip, port = address.split(":")
        return ip, port or None
    else:
        return address, None

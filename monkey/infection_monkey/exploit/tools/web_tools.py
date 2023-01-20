from posixpath import join
from typing import List, Optional, Tuple


def build_urls(
    ip: str, ports: List[Tuple[str, bool]], extensions: Optional[List[str]] = None
) -> List[str]:
    """
    Build all possibly-vulnerable URLs on a specific host, based on the relevant ports and
    extensions.
    :param ip: IP address of the victim
    :param ports: Array of ports. One port is described as size 2 array: [port.no(int),
    isHTTPS?(bool)]
    Eg. ports: [[80, False], [443, True]]
    :param extensions: What subdirectories to scan. www.domain.com[/extension]
    :return: Array of url's to try and attack
    """
    url_list = []
    if extensions:
        extensions = [(e[1:] if "/" == e[0] else e) for e in extensions]
    else:
        extensions = [""]
    for port in ports:
        for extension in extensions:
            if port[1]:
                protocol = "https"
            else:
                protocol = "http"
            url_list.append(join(("%s://%s:%s" % (protocol, ip, port[0])), extension))
    return url_list

import re
from urllib.parse import urlparse


def get_host_from_network_location(network_location: str) -> str:
    """
    URL structure is "<scheme>://<net_loc>/<path>;<params>?<query>#<fragment>" (https://tools.ietf.org/html/rfc1808.html)
    And the net_loc is "<user>:<password>@<host>:<port>" (https://tools.ietf.org/html/rfc1738#section-3.1)
    :param network_location:  server network location
    :return:  host part of the network location
    """
    url = urlparse("http://" + network_location)
    return str(url.hostname)


def remove_port(url):
    parsed = urlparse(url)
    with_port = f'{parsed.scheme}://{parsed.netloc}'
    without_port = re.sub(':[0-9]+(?=$|\/)', '', with_port)
    return without_port

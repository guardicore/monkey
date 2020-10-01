import re
from urllib.parse import urlparse

from infection_monkey.config import WormConfiguration
from infection_monkey.network.tools import is_running_on_server


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


def is_running_on_island():
    current_server_without_port = get_host_from_network_location(WormConfiguration.current_server)
    running_on_island = is_running_on_server(current_server_without_port)
    return running_on_island and WormConfiguration.depth == WormConfiguration.max_depth

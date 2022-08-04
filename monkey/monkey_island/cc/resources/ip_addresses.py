from typing import Sequence

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class IpAddresses(AbstractResource):
    """
    Endpoint for the Monkey Island's local IP addresses
    """

    urls = ["/api/island/ip-addresses"]

    def __init__(self, local_ip_addresses: Sequence[str]):
        self._local_ips = local_ip_addresses

    @jwt_required
    def get(self) -> Sequence[str]:
        """
        Sends the local IP addresses of the Island

        :return: Local IPs
        """

        return self._local_ips

from typing import Sequence

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class IPAddresses(AbstractResource):
    """
    Endpoint for the Monkey Island's IP addresses
    """

    urls = ["/api/island/ip-addresses"]

    def __init__(self, ip_addresses: Sequence[str]):
        self._ips = ip_addresses

    @jwt_required
    def get(self) -> Sequence[str]:
        """
        Sends the IP addresses of the Island

        :return: IP addresses
        """

        return self._ips

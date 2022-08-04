from typing import Mapping, Sequence

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class IpAddresses(AbstractResource):
    urls = ["/api/island/ip-addresses"]

    def __init__(self, local_ip_addresses: Sequence[str]):
        self._local_ips = local_ip_addresses

    @jwt_required
    def get(self) -> Mapping[str, Sequence[str]]:
        """
        Gets the IP addresses of the Island network interfaces

        :return: a dictionary with "ip_addresses" key that points to a list of IP's
        """

        return {"ip_addresses": self._local_ips}

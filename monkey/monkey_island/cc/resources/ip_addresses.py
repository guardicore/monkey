from typing import Mapping, Sequence

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.utils.network_utils import get_local_ip_addresses


class IpAddresses(AbstractResource):
    urls = ["/api/island/ip-addresses"]

    @jwt_required
    def get(self) -> Mapping[str, Sequence[str]]:
        """
        Gets the IP addresses of the Island network interfaces

        :return: a dictionary with "ip_addresses" key that points to a list of IP's
        """
        local_ips = get_local_ip_addresses()

        return {"ip_addresses": local_ips}

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.utils.network_utils import local_ip_addresses


class IpAddresses(AbstractResource):
    urls = ["/api/island/ip-addresses"]

    @jwt_required
    def get(self):
        """
        Gets the local ip address from the Island

        :return: a list of local ips
        """
        local_ips = local_ip_addresses()

        return {"ip_addresses": local_ips}

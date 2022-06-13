from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.services.utils.network_utils import local_ip_addresses


class LocalIps(AbstractResource):
    urls = ["/api/island/local-ips"]

    @jwt_required
    def get(self):
        """
        Gets the local ip address from the Island

        :return: a list of local ips
        """
        local_ips = local_ip_addresses()

        return {"local_ips": local_ips}

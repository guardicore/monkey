import logging

import infection_monkey.config
from infection_monkey.network.HostFinger import HostFinger

LOG = logging.getLogger(__name__)


class HTTPFinger(HostFinger):
    """
    Goal is to recognise HTTP servers, where what we currently care about is apache.
    """
    _SCANNED_SERVICE = 'HTTP'

    def __init__(self):
        self._config = infection_monkey.config.WormConfiguration
        self.HTTP = [(port, str(port)) for port in self._config.HTTP_PORTS]

    @staticmethod
    def _banner_match(service, host, banner):
        pass

    def get_host_fingerprint(self, host):
        from contextlib import closing

        from requests import head
        from requests.exceptions import ConnectionError, Timeout

        for port in self.HTTP:
            # check both http and https
            http = "http://" + host.ip_addr + ":" + port[1]
            https = "https://" + host.ip_addr + ":" + port[1]

            # try http, we don't optimise for 443
            for url in (https, http):  # start with https and downgrade
                try:
                    with closing(head(url, verify=False, timeout=1)) as req:  # noqa: DUO123
                        server = req.headers.get('Server')
                        ssl = True if 'https://' in url else False
                        self.init_service(host.services, ('tcp-' + port[1]), port[0])
                        host.services['tcp-' + port[1]]['name'] = 'http'
                        host.services['tcp-' + port[1]]['data'] = (server, ssl)
                        LOG.info("Port %d is open on host %s " % (port[0], host))
                        break  # https will be the same on the same port
                except Timeout:
                    pass
                except ConnectionError:  # Someone doesn't like us
                    pass

        return True

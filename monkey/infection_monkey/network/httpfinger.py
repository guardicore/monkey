import infection_monkey.config
from infection_monkey.network import HostFinger
from infection_monkey.model.host import VictimHost
from infection_monkey.transport.attack_telems.victim_host_telem import VictimHostTelem
from common.utils.attack_utils import ScanStatus
import logging

LOG = logging.getLogger(__name__)


class HTTPFinger(HostFinger):
    """
    Goal is to recognise HTTP servers, where what we currently care about is apache.
    """

    def __init__(self):
        self._config = infection_monkey.config.WormConfiguration
        self.HTTP = [(port, str(port)) for port in self._config.HTTP_PORTS]

    @staticmethod
    def _banner_match(service, host, banner):
        pass

    def get_host_fingerprint(self, host):
        assert isinstance(host, VictimHost)
        from requests import head
        from requests.exceptions import Timeout, ConnectionError
        from contextlib import closing

        for port in self.HTTP:
            # check both http and https
            http = "http://" + host.ip_addr + ":" + port[1]
            https = "https://" + host.ip_addr + ":" + port[1]

            # try http, we don't optimise for 443
            for url in (https, http):  # start with https and downgrade
                try:
                    with closing(head(url, verify=False, timeout=1)) as req:
                        server = req.headers.get('Server')
                        ssl = True if 'https://' in url else False
                        host.services['tcp-' + port[1]] = {}
                        host.services['tcp-' + port[1]]['name'] = 'http'
                        host.services['tcp-' + port[1]]['data'] = (server,ssl)
                        LOG.info("Port %d is open on host %s " % (port[0], host))
                        VictimHostTelem('T1210', ScanStatus.SCANNED.value,
                                        host, {'port': port[0], 'service': 'HTTP/HTTPS'}).send()
                        break  # https will be the same on the same port
                except Timeout:
                    pass
                except ConnectionError:  # Someone doesn't like us
                    pass

        return True

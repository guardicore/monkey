from network import HostFinger


class HTTPFinger(HostFinger):
    """
    Goal is to recognise HTTP servers, where what we currently care about is apache.
    """

    def __init__(self):
        self._config = __import__('config').WormConfiguration
        self.HTTP = [(port, str(port)) for port in self._config.HTTP_PORTS]

    @staticmethod
    def _banner_match(service, host, banner):
        pass

    def get_host_fingerprint(self, host):
        assert isinstance(host, VictimHost)
        from requests import get
        from requests.exceptions import Timeout, ConnectionError
        from contextlib import closing

        for port in self.HTTP:
            # check both http and https
            http = "http://" + host.ip_addr + ":" + port[1]
            https = "https://" + host.ip_addr + ":" + port[1]

            # try http, we don't optimise for 443
            for url in (http, https):
                try:
                    with closing(get(url, verify=False, timeout=1, stream=True)) as req:
                        server = req.headers.get('Server')
                        host.services['tcp-' + port[1]] = server
                        break  # https will be the same on the same port
                except Timeout:
                    pass
                except ConnectionError:  # Someone doesn't like us
                    pass

        return True

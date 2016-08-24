import re
from network import HostFinger
from network.tools import check_port_tcp
from model.host import VictimHost



class HTTPFinger(HostFinger):
    '''
    Goal is to recognise HTTP servers, where what we currently care about is apache.
    '''
    def __init__(self):
        self._config = __import__('config').WormConfiguration
        self.HTTP = [(port,str(port)) for port in self._config.HTTP_PORTS]


    @staticmethod
    def _banner_match(service, host, banner):
        pass

    def get_host_fingerprint(self, host):
        assert isinstance(host, VictimHost)
        from requests import get
        from requests.exceptions import Timeout
        from contextlib import closing

        valid_ports = [port for port in self.HTTP if 'tcp-'+port[1] in host.services]
        for port in valid_ports:
            # check both http and https
            http = "http://"+host.ip_addr+":"+port[1]
            https = "https://"+host.ip_addr+":"+port[1]

            # try http, we don't optimise for 443
            try:
                with closing(get(http, timeout=1, stream=True)) as r_http:
                    server = r_http.headers.get('Server')
                    host.services['tcp-'+port[1]] = server
            except Timeout:
                #try https
                with closing(get(https, timeout=01, stream=True)) as r_http:
                    server = r_http.headers.get('Server')
                    host.services['tcp-'+port[1]] = server

        return True
import json
import logging
from contextlib import closing

import requests
from requests.exceptions import Timeout, ConnectionError

from model.host import VictimHost
from network import HostFinger

ES_PORT = 9200
ES_SERVICE = 'elastic-search-9200'
ES_HTTP_TIMEOUT = 5
LOG = logging.getLogger(__name__)
__author__ = 'danielg'


class ElasticFinger(HostFinger):
    """
        Fingerprints elastic search clusters, only on port 9200
    """

    def __init__(self):
        self._config = __import__('config').WormConfiguration

    def get_host_fingerprint(self, host):
        """
        Returns elasticsearch metadata
        :param host:
        :return: Success/failure, data is saved in the host struct
        """
        assert isinstance(host, VictimHost)
        try:
            url = 'http://%s:%s/' % (host.ip_addr, ES_PORT)
            with closing(requests.get(url, timeout=ES_HTTP_TIMEOUT)) as req:
                data = json.loads(req.text)
                host.services[ES_SERVICE] = {}
                host.services[ES_SERVICE]['cluster_name'] = data['cluster_name']
                host.services[ES_SERVICE]['name'] = data['name']
                host.services[ES_SERVICE]['version'] = data['version']['number']
                return True
        except Timeout:
            LOG.debug("Got timeout while trying to read header information")
        except ConnectionError:  # Someone doesn't like us
            LOG.debug("Unknown connection error")
        except KeyError:
            LOG.debug("Failed parsing the ElasticSearch JSOn response")
        return False

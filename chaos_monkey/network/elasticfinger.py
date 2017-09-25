import json
import logging
from contextlib import closing

import requests
from requests.exceptions import Timeout, ConnectionError

from model.host import VictimHost
from network import HostFinger

ES_PORT = 9200
ES_SERVICE = 'es-3306'

LOG = logging.getLogger(__name__)
__author__ = 'danielg'


class ElasticFinger(HostFinger):
    """
        Fingerprints mysql databases, only on port 3306
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
            with closing(requests.get(url, timeout=1)) as req:
                data = json.loads(req.text)
                host.services[ES_SERVICE] = {}
                host.services[ES_SERVICE]['name'] = 'ElasticSearch'
                host.services[ES_SERVICE]['cluster_name'] = data['name']
                host.services[ES_SERVICE]['version'] = data['version']['number']
                return True
        except Timeout:
            LOG.debug("Got timeout while trying to read header information")
        except ConnectionError:  # Someone doesn't like us
            LOG.debug("Unknown connection error")
        except KeyError:
            LOG.debug("Failed parsing the ElasticSearch JSOn response")
        return False

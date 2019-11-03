import json
import logging
from contextlib import closing

import requests
from requests.exceptions import Timeout, ConnectionError

import infection_monkey.config
import infection_monkey.network.HostFinger
from common.data.network_consts import ES_SERVICE

ES_PORT = 9200
ES_HTTP_TIMEOUT = 5
LOG = logging.getLogger(__name__)
__author__ = 'danielg'


class ElasticFinger(infection_monkey.network.HostFinger.HostFinger):
    """
        Fingerprints elastic search clusters, only on port 9200
    """
    _SCANNED_SERVICE = 'Elastic search'

    def __init__(self):
        self._config = infection_monkey.config.WormConfiguration

    def get_host_fingerprint(self, host):
        """
        Returns elasticsearch metadata
        :param host:
        :return: Success/failure, data is saved in the host struct
        """
        try:
            url = 'http://%s:%s/' % (host.ip_addr, ES_PORT)
            with closing(requests.get(url, timeout=ES_HTTP_TIMEOUT)) as req:
                data = json.loads(req.text)
                self.init_service(host.services, ES_SERVICE, ES_PORT)
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

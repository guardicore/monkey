import json
import logging
from contextlib import closing

import requests
from requests.exceptions import Timeout, ConnectionError

import infection_monkey.config
from infection_monkey.model.host import VictimHost
from infection_monkey.network import HostFinger
from common.utils.attack_utils import ScanStatus
from infection_monkey.transport.attack_telems.victim_host_telem import VictimHostTelem

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
        self._config = infection_monkey.config.WormConfiguration

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
                VictimHostTelem('T1210', ScanStatus.SCANNED.value,
                                host, {'port': ES_PORT, 'service': 'Elastic'}).send()
                return True
        except Timeout:
            LOG.debug("Got timeout while trying to read header information")
        except ConnectionError:  # Someone doesn't like us
            LOG.debug("Unknown connection error")
        except KeyError:
            LOG.debug("Failed parsing the ElasticSearch JSOn response")
        return False

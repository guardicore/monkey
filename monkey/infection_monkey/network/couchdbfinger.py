import json
import logging
from contextlib import closing

import requests
from requests.exceptions import ConnectionError, Timeout

import infection_monkey.config
from common.common_consts.network_consts import CDB_SERVICE
from infection_monkey.network.HostFinger import HostFinger

CDB_PORT = 5984
CDB_HTTP_TIMEOUT = 5
LOG = logging.getLogger(__name__)


class CouchDBFinger(HostFinger):
    """
    Fingerprints couchdb search, only on port 5984
    """

    _SCANNED_SERVICE = "CouchDB"

    def __init__(self):
        self._config = infection_monkey.config.WormConfiguration

    def get_host_fingerprint(self, host):
        """
        Returns couchdb metadata
        :param host:
        :return: Success/failure, data is saved in the host struct
        """
        try:
            url = "http://%s:%s/" % (host.ip_addr, CDB_PORT)
            with closing(requests.get(url, timeout=CDB_HTTP_TIMEOUT)) as req:
                data = json.loads(req.text)
                self.init_service(host.services, CDB_SERVICE, CDB_PORT)
                host.services[CDB_SERVICE]["cluster_name"] = data["cluster_name"]
                host.services[CDB_SERVICE]["name"] = data["name"]
                host.services[CDB_SERVICE]["version"] = data["version"]["number"]
                return True
        except Timeout:
            LOG.debug("Got timeout while trying to read header information")
        except ConnectionError:  # Someone doesn't like us
            LOG.debug("Unknown connection error")
        except KeyError:
            LOG.debug("Failed parsing the Apache CouchDB JSOn response")
        return False

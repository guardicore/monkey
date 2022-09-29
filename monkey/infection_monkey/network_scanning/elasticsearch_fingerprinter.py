import logging
from contextlib import closing
from typing import Any, Dict

import requests

from common.common_consts.network_consts import ES_SERVICE
from common.types import PingScanData, PortStatus
from infection_monkey.i_puppet import FingerprintData, IFingerprinter, PortScanData

DISPLAY_NAME = "ElasticSearch"
ES_PORT = 9200
ES_HTTP_TIMEOUT = 5
logger = logging.getLogger(__name__)


class ElasticSearchFingerprinter(IFingerprinter):
    """
    Fingerprints elastic search clusters, only on port 9200
    """

    def get_host_fingerprint(
        self,
        host: str,
        _ping_scan_data: PingScanData,
        port_scan_data: Dict[int, PortScanData],
        _options: Dict,
    ) -> FingerprintData:
        services = {}

        if (ES_PORT not in port_scan_data) or (port_scan_data[ES_PORT].status != PortStatus.OPEN):
            return FingerprintData(None, None, services)

        try:
            elasticsearch_info = _query_elasticsearch(host)
            services[ES_SERVICE] = _get_service_from_query_info(elasticsearch_info)
        except Exception as ex:
            logger.debug(f"Did not detect an ElasticSearch cluster: {ex}")

        return FingerprintData(None, None, services)


def _query_elasticsearch(host: str) -> Dict[str, Any]:
    url = "http://%s:%s/" % (host, ES_PORT)
    logger.debug(f"Sending request to {url}")
    with closing(requests.get(url, timeout=ES_HTTP_TIMEOUT)) as response:
        return response.json()


def _get_service_from_query_info(elasticsearch_info: Dict[str, Any]) -> Dict[str, Any]:
    try:
        return {
            "display_name": DISPLAY_NAME,
            "port": ES_PORT,
            "cluster_name": elasticsearch_info["cluster_name"],
            "name": elasticsearch_info["name"],
            "version": elasticsearch_info["version"]["number"],
        }
    except KeyError as ke:
        raise Exception(f"Unable to find the key {ke} in the server's response") from ke

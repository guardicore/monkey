import logging
from contextlib import closing
from typing import Dict, Iterable, Optional, Set

from requests import head
from requests.exceptions import ConnectionError, Timeout
from requests.structures import CaseInsensitiveDict

from common.event_queue import IAgentEventPublisher
from common.types import (
    AgentID,
    DiscoveredService,
    NetworkPort,
    NetworkProtocol,
    NetworkService,
    PortStatus,
)
from infection_monkey.i_puppet import FingerprintData, IFingerprinter, PingScanData, PortScanData

logger = logging.getLogger(__name__)


class HTTPFingerprinter(IFingerprinter):
    """
    Queries potential HTTP(S) ports and attempt to determine the server software that handles the
    HTTP requests.
    """

    def __init__(self, agent_id: AgentID, agent_event_publisher: IAgentEventPublisher):
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher

    def get_host_fingerprint(
        self,
        host: str,
        _: PingScanData,
        port_scan_data: Dict[int, PortScanData],
        options: Dict,
    ) -> FingerprintData:
        services = []
        http_ports = set(options.get("http_ports", []))
        ports_to_fingerprint = _get_open_http_ports(http_ports, port_scan_data)

        for port in ports_to_fingerprint:
            service = _query_potential_http_server(host, port)

            if service:
                services.append(
                    DiscoveredService(
                        protocol=NetworkProtocol.TCP, port=NetworkPort(port), service=service
                    )
                )

        return FingerprintData(os_type=None, os_version=None, services=services)


def _query_potential_http_server(host: str, port: int) -> Optional[NetworkService]:
    # check both http and https
    http = f"http://{host}:{port}"
    https = f"https://{host}:{port}"

    for url, ssl in ((https, True), (http, False)):  # start with https and downgrade
        server_header = _get_server_from_headers(url)

        if server_header is not None:
            return NetworkService.HTTPS if ssl else NetworkService.HTTP

    return None


def _get_server_from_headers(url: str) -> Optional[str]:
    headers = _get_http_headers(url)
    if headers:
        return headers.get("Server", "")

    return None


def _get_http_headers(url: str) -> Optional[CaseInsensitiveDict]:
    try:
        logger.debug(f"Sending request for headers to {url}")
        with closing(head(url, verify=False, timeout=1)) as response:  # noqa: DUO123
            return response.headers
    except Timeout:
        logger.debug(f"Timeout while requesting headers from {url}")
    except ConnectionError:  # Someone doesn't like us
        logger.debug(f"Connection error while requesting headers from {url}")

    return None


def _get_open_http_ports(
    allowed_http_ports: Set, port_scan_data: Dict[int, PortScanData]
) -> Iterable[int]:
    open_ports = (psd.port for psd in port_scan_data.values() if psd.status == PortStatus.OPEN)
    return (port for port in open_ports if port in allowed_http_ports)

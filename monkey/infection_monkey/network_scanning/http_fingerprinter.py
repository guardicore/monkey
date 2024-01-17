import logging
import time
from contextlib import closing
from http import HTTPMethod
from ipaddress import IPv4Address
from typing import Dict, Optional, Sequence, Set

from agentpluginapi import PortScanData
from monkeyevents import FingerprintingEvent, HTTPRequestEvent
from monkeyevents.tags import ACTIVE_SCANNING_T1595_TAG, GATHER_VICTIM_HOST_INFORMATION_T1592_TAG
from monkeytypes import (
    AgentID,
    DiscoveredService,
    NetworkPort,
    NetworkProtocol,
    NetworkService,
    PortStatus,
)
from requests import head
from requests.exceptions import ConnectionError, Timeout
from requests.structures import CaseInsensitiveDict

from common.event_queue import IAgentEventPublisher
from infection_monkey.i_puppet import FingerprintData, IFingerprinter, PingScanData

logger = logging.getLogger(__name__)

HTTP_FINGERPRINTER_TAG = "http-fingerprinter"
EVENT_TAGS = frozenset(
    {HTTP_FINGERPRINTER_TAG, ACTIVE_SCANNING_T1595_TAG, GATHER_VICTIM_HOST_INFORMATION_T1592_TAG}
)


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

        timestamp = time.time()
        for port in ports_to_fingerprint:
            service = self._query_potential_http_server(host, port)

            if service:
                services.append(
                    DiscoveredService(
                        protocol=NetworkProtocol.TCP, port=NetworkPort(port), service=service
                    )
                )

        # If there were no ports worth fingerprinting (i.e. no actual fingerprinting action took
        # place), then we don't want to publish an event.
        if len(ports_to_fingerprint) > 0:
            self._publish_fingerprinting_event(host, timestamp, services)

        return FingerprintData(os_type=None, os_version=None, services=services)

    def _query_potential_http_server(self, host: str, port: int) -> Optional[NetworkService]:
        # check both http and https
        http = f"http://{host}:{port}"
        https = f"https://{host}:{port}"

        for url, ssl in ((https, True), (http, False)):  # start with https and downgrade
            server_header = self._get_server_from_headers(host, url)

            if server_header is not None:
                return NetworkService.HTTPS if ssl else NetworkService.HTTP

        return None

    def _get_server_from_headers(self, host: str, url: str) -> Optional[str]:
        timestamp = time.time()
        headers = _get_http_headers(url)
        self._publish_http_request_event(host, timestamp, url)

        if headers:
            return headers.get("Server", "")

        return None

    def _publish_http_request_event(self, host: str, timestamp: float, url: str):
        self._agent_event_publisher.publish(
            HTTPRequestEvent(
                source=self._agent_id,
                target=IPv4Address(host),
                timestamp=timestamp,
                tags=EVENT_TAGS,  # type: ignore [arg-type]
                method=HTTPMethod.HEAD,
                url=url,  # type: ignore [arg-type]
            )
        )

    def _publish_fingerprinting_event(
        self, host: str, timestamp: float, discovered_services: Sequence[DiscoveredService]
    ):
        self._agent_event_publisher.publish(
            FingerprintingEvent(
                source=self._agent_id,
                target=IPv4Address(host),
                timestamp=timestamp,
                tags=EVENT_TAGS,  # type: ignore [arg-type]
                os=None,
                os_version=None,
                discovered_services=tuple(discovered_services),
            )
        )


def _get_open_http_ports(
    allowed_http_ports: Set, port_scan_data: Dict[int, PortScanData]
) -> Sequence[int]:
    open_ports = (psd.port for psd in port_scan_data.values() if psd.status == PortStatus.OPEN)
    return [port for port in open_ports if port in allowed_http_ports]


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

import logging
from contextlib import closing
from typing import Dict, Iterable, Optional, Set, Tuple

from requests import head
from requests.exceptions import ConnectionError, Timeout

from infection_monkey.i_puppet import (
    FingerprintData,
    IFingerprinter,
    PingScanData,
    PortScanData,
    PortStatus,
)

logger = logging.getLogger(__name__)


class HTTPFingerprinter(IFingerprinter):
    """
    Goal is to recognise HTTP servers, where what we currently care about is apache.
    """

    def get_host_fingerprint(
        self,
        host: str,
        _: PingScanData,
        port_scan_data: Dict[int, PortScanData],
        options: Dict,
    ):
        services = {}
        http_ports = set(options.get("http_ports", []))
        ports_to_fingerprint = _get_open_http_ports(http_ports, port_scan_data)

        for port in ports_to_fingerprint:
            server_header_contents, ssl = _query_potential_http_server(host, port)

            if server_header_contents is not None:
                services[f"tcp-{port}"] = {
                    "display_name": "HTTP",
                    "port": port,
                    "name": "http",
                    "data": (server_header_contents, ssl),
                }

        return FingerprintData(None, None, services)


def _query_potential_http_server(host: str, port: int) -> Tuple[Optional[str], Optional[bool]]:
    # check both http and https
    http = f"http://{host}:{port}"
    https = f"https://{host}:{port}"

    # try http, we don't optimise for 443
    for url, ssl in ((https, True), (http, False)):  # start with https and downgrade
        server_header_contents = _get_server_from_headers(url)

        if server_header_contents is not None:
            return (server_header_contents, ssl)

    return (None, None)


def _get_server_from_headers(url: str) -> Optional[str]:
    try:
        logger.debug(f"Sending request for headers to {url}")
        with closing(head(url, verify=False, timeout=1)) as req:  # noqa: DUO123
            server = req.headers.get("Server")

            logger.debug(f'Got server string "{server}" from {url}')
            return server
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

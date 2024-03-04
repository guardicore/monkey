import errno
import logging
import socket
import time
from ipaddress import IPv4Address
from typing import Dict, Optional, Sequence, Set

from agentpluginapi import FingerprintData, IAgentEventPublisher, PingScanData, PortScanData
from monkeyevents import FingerprintingEvent
from monkeyevents.tags import ACTIVE_SCANNING_T1595_TAG, GATHER_VICTIM_HOST_INFORMATION_T1592_TAG
from monkeytypes import AgentID, DiscoveredService, NetworkPort, NetworkProtocol, NetworkService

from infection_monkey.i_puppet import IFingerprinter

SQL_BROWSER_DEFAULT_PORT = NetworkPort(1434)
_BUFFER_SIZE = 4096
_MSSQL_SOCKET_TIMEOUT = 5

MSSQL_FINGERPRINTER_TAG = "mssql-fingerprinter"
EVENT_TAGS = frozenset(
    {MSSQL_FINGERPRINTER_TAG, ACTIVE_SCANNING_T1595_TAG, GATHER_VICTIM_HOST_INFORMATION_T1592_TAG}
)

logger = logging.getLogger(__name__)


class MSSQLFingerprinter(IFingerprinter):
    def __init__(self, agent_id: AgentID, agent_event_publisher: IAgentEventPublisher):
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher

    def get_host_fingerprint(
        self,
        host: str,
        _: PingScanData,
        port_scan_data: Dict[int, PortScanData],
        options: Dict,
    ):
        """Gets Microsoft SQL Server instance information by querying the SQL Browser service."""
        services: Set[DiscoveredService] = set()

        timestamp = time.time()
        try:
            data = _query_mssql_for_instance_data(host, services)
            _get_services_from_server_data(data, services)

        except Exception as ex:
            logger.debug(f"Did not detect an MSSQL server: {ex}")

        self._publish_fingerprinting_event(host, timestamp, list(services))

        return FingerprintData(os_type=None, os_version=None, services=list(services))

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


def _query_mssql_for_instance_data(host: str, services: Set[DiscoveredService]) -> bytes:
    # Create a UDP socket and sets a timeout
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(_MSSQL_SOCKET_TIMEOUT)

    server_address = (host, SQL_BROWSER_DEFAULT_PORT)

    # The message is a CLNT_UCAST_EX packet to get all instances
    # https://msdn.microsoft.com/en-us/library/cc219745.aspx
    request = "\x03"

    # Encode the message as a bytes array
    message = request.encode()

    # send data and receive response
    try:
        logger.info(f"Sending message to requested host: {host}, {message!r}")
        sock.sendto(message, server_address)
        data, _ = sock.recvfrom(_BUFFER_SIZE)

        services.add(
            DiscoveredService(
                protocol=NetworkProtocol.UDP,
                port=SQL_BROWSER_DEFAULT_PORT,
                service=NetworkService.UNKNOWN,
            )
        )

        return data
    except socket.timeout as err:
        logger.debug(f"Socket timeout reached, maybe browser service on host: {host} doesn't exist")
        raise err
    except socket.error as err:
        if err.errno == errno.ECONNRESET:
            error_message = (
                f"Connection was forcibly closed by the remote host. The host: {host} is "
                "rejecting the packet."
            )
        else:
            error_message = (
                "An unknown socket error occurred while trying the mssql fingerprint, "
                "closing socket."
            )
        raise Exception(error_message) from err
    finally:
        sock.close()


def _get_tcp_port_from_response(response: str) -> Optional[NetworkPort]:
    response_info = response.split(";")
    try:
        return NetworkPort(response_info[response_info.index("tcp") + 1])
    except (KeyError, ValueError):
        logger.warning(
            "Got a malformed response from MSSQL server, "
            "fingerprinter failed to locate the TCP port"
        )
        return None


def _get_services_from_server_data(data: bytes, services: Set[DiscoveredService]):
    mssql_responses = filter(lambda i: i != "", data[3:].decode().split(";;"))
    for response in mssql_responses:
        response_tcp_port = _get_tcp_port_from_response(response)
        if response_tcp_port:
            services.add(
                DiscoveredService(
                    protocol=NetworkProtocol.TCP,
                    port=response_tcp_port,
                    service=NetworkService.MSSQL,
                )
            )
            services.add(
                DiscoveredService(
                    protocol=NetworkProtocol.UDP,
                    port=SQL_BROWSER_DEFAULT_PORT,
                    service=NetworkService.MSSQL_BROWSER,
                )
            )

        logger.debug(f"An MSSQL response has been recieved: {response}")

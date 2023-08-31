import errno
import logging
import socket
from typing import Dict, Optional, Set

from common.types import DiscoveredService, NetworkPort, NetworkProtocol, NetworkService
from infection_monkey.i_puppet import FingerprintData, IFingerprinter, PingScanData, PortScanData

SQL_BROWSER_DEFAULT_PORT = NetworkPort(1434)
_BUFFER_SIZE = 4096
_MSSQL_SOCKET_TIMEOUT = 5

logger = logging.getLogger(__name__)


class MSSQLFingerprinter(IFingerprinter):
    def get_host_fingerprint(
        self,
        host: str,
        _: PingScanData,
        port_scan_data: Dict[int, PortScanData],
        options: Dict,
    ):
        """Gets Microsoft SQL Server instance information by querying the SQL Browser service."""
        services: Set[DiscoveredService] = set()

        try:
            data = _query_mssql_for_instance_data(host, services)
            _get_services_from_server_data(data, services)

        except Exception as ex:
            logger.debug(f"Did not detect an MSSQL server: {ex}")

        return FingerprintData(os_type=None, os_version=None, services=list(services))


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

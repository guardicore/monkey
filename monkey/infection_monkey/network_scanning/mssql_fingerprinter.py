import errno
import logging
import socket
from typing import Dict, List, Sequence

from common.types import NetworkPort, NetworkProtocol, NetworkService
from infection_monkey.i_puppet import (
    DiscoveredService,
    FingerprintData,
    IFingerprinter,
    PingScanData,
    PortScanData,
)

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
        services = []

        try:
            data = _query_mssql_for_instance_data(host)
            services = _get_services_from_server_data(data)

        except Exception as ex:
            logger.debug(f"Did not detect an MSSQL server: {ex}")

        return FingerprintData(os_type=None, os_version=None, services=services)


def _query_mssql_for_instance_data(host: str) -> bytes:
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


def _get_instance_info(instance_info: Sequence[str]) -> Dict[str, str]:
    info = {}
    it = iter(instance_info)
    for k in it:
        info[k] = next(it)

    return info


def _parse_instance(instance: str) -> Dict[str, str]:
    instance_info = instance.split(";")
    if len(instance_info) > 1:
        return _get_instance_info(instance_info)

    return {}


def _get_services_from_server_data(data: bytes) -> List[DiscoveredService]:
    services = []

    # Loop through the server data
    # Example data:
    # yServerName;MSSQL-16;InstanceName;MSSQLSERVER;IsClustered;No;Version;14.0.1000.169;tcp;1433;np;\\MSSQL-16\pipe\sql\query;;
    mssql_instances = filter(lambda i: i != "", data[3:].decode().split(";;"))
    for instance in mssql_instances:

        instance_info = _parse_instance(instance)
        if "tcp" in instance_info:
            services.append(
                DiscoveredService(
                    protocol=NetworkProtocol.TCP,
                    port=NetworkPort(instance_info["tcp"]),
                    services=NetworkService.MSSQL,
                )
            )
        logger.debug(f"Found MSSQL instance: {instance}")

    if not services:
        services.append(
            DiscoveredService(
                protocol=NetworkProtocol.UDP,
                port=SQL_BROWSER_DEFAULT_PORT,
                services=NetworkService.UNKNOWN,
            )
        )

    return services

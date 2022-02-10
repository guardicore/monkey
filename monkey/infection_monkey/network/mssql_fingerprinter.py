import errno
import logging
import socket
from typing import Any, Dict, Optional

from infection_monkey.i_puppet import FingerprintData, IFingerprinter, PingScanData, PortScanData

MSSQL_SERVICE = "MSSQL"
DISPLAY_NAME = MSSQL_SERVICE
SQL_BROWSER_DEFAULT_PORT = 1434
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
        services = {}

        try:
            data = _query_mssql_for_instance_data(host)
            services = _get_services_from_server_data(data)

        except Exception as ex:
            logger.debug(f"Did not detect an MSSQL server: {ex}")

        return FingerprintData(None, None, services)


def _query_mssql_for_instance_data(host: str) -> Optional[bytes]:
    # Create a UDP socket and sets a timeout
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(_MSSQL_SOCKET_TIMEOUT)

    server_address = (host, SQL_BROWSER_DEFAULT_PORT)

    # The message is a CLNT_UCAST_EX packet to get all instances
    # https://msdn.microsoft.com/en-us/library/cc219745.aspx
    message = "\x03"

    # Encode the message as a bytes array
    message = message.encode()

    # send data and receive response
    try:
        logger.info(f"Sending message to requested host: {host}, {message}")
        sock.sendto(message, server_address)
        data, _ = sock.recvfrom(_BUFFER_SIZE)

        return data
    except socket.timeout as err:
        logger.debug(
            f"Socket timeout reached, maybe browser service on host: {host} doesnt " "exist"
        )
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


def _get_services_from_server_data(data: bytes) -> Dict[str, Any]:
    services = {MSSQL_SERVICE: {}}
    services[MSSQL_SERVICE]["display_name"] = DISPLAY_NAME
    services[MSSQL_SERVICE]["port"] = SQL_BROWSER_DEFAULT_PORT

    # Loop through the server data
    mssql_instances = filter(lambda i: i != "", data[3:].decode().split(";;"))

    for instance in mssql_instances:
        instance_info = instance.split(";")
        if len(instance_info) > 1:
            services[MSSQL_SERVICE][instance_info[1]] = {}
            for i in range(1, len(instance_info), 2):
                # Each instance's info is nested under its own name, if there are multiple
                # instances
                # each will appear under its own name
                services[MSSQL_SERVICE][instance_info[1]][instance_info[i - 1]] = instance_info[i]

            logger.debug(f"Found MSSQL instance: {instance}")

    if len(services[MSSQL_SERVICE].keys()) == 2:
        services = {}

    return services

import logging
import socket

from model.host import VictimHost
from network import HostFinger


LOG = logging.getLogger(__name__)


class MSSQLFingerprint(HostFinger):

    # Class related consts
    SQL_BROWSER_DEFAULT_PORT = 1434
    BUFFER_SIZE = 4096
    TIMEOUT = 5
    SERVICE_NAME = 'mssql'

    def __init__(self):
        self._config = __import__('config').WormConfiguration

    def get_host_fingerprint(self, host):
        """Gets Microsoft SQL Server instance information by querying the SQL Browser service.
            Args:
                host (str): Hostname or IP address of the SQL Server to query for information.

            Returns:
                Discovered server information written to the Host info struct.
        """

        assert isinstance(host, VictimHost)

        # Create a UDP socket and sets a timeout
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.TIMEOUT)
        server_address = (str(host), self.SQL_BROWSER_DEFAULT_PORT)

        # The message is a CLNT_UCAST_EX packet to get all instances
        # https://msdn.microsoft.com/en-us/library/cc219745.aspx
        message = '\x03'

        # Encode the message as a bytesarray
        message = message.encode()

        # send data and receive response
        results = []
        try:
            LOG.info('Sending message to requested host: {0}, {1}'.format(host, message))
            sock.sendto(message, server_address)
            data, server = sock.recvfrom(self.BUFFER_SIZE)
        except socket.timeout:
            LOG.error('Socket timeout reached, maybe browser service on host: {0} doesnt exist'.format(host))
            sock.close()
            return results

        host.services[self.SERVICE_NAME] = {}

        # Loop through the server data
        for server in data[3:].decode().split(';;'):
            instance_info = server.split(';')
            if len(instance_info) > 1:
                for i in range(1, len(instance_info), 2):
                    host.services[self.SERVICE_NAME][instance_info[i - 1]] = instance_info[i]

        # Close the socket
        sock.close()

        return results

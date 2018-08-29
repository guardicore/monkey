import logging
import socket

from model.host import VictimHost
from network import HostFinger

__author__ = 'Maor Rayzin'

LOG = logging.getLogger(__name__)


class MSSQLFinger(HostFinger):

    # Class related consts
    SQL_BROWSER_DEFAULT_PORT = 1434
    BUFFER_SIZE = 4096
    TIMEOUT = 5
    SERVICE_NAME = 'MSSQL'

    def __init__(self):
        self._config = __import__('config').WormConfiguration

    def get_host_fingerprint(self, host):
        """Gets Microsoft SQL Server instance information by querying the SQL Browser service.
            :arg:
                host (VictimHost): The MS-SSQL Server to query for information.

            :returns:
                Discovered server information written to the Host info struct.
                True if success, False otherwise.
        """

        assert isinstance(host, VictimHost)

        # Create a UDP socket and sets a timeout
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.TIMEOUT)
        server_address = (str(host.ip_addr), self.SQL_BROWSER_DEFAULT_PORT)

        # The message is a CLNT_UCAST_EX packet to get all instances
        # https://msdn.microsoft.com/en-us/library/cc219745.aspx
        message = '\x03'

        # Encode the message as a bytesarray
        message = message.encode()

        # send data and receive response
        try:
            LOG.info('Sending message to requested host: {0}, {1}'.format(host, message))
            sock.sendto(message, server_address)
            data, server = sock.recvfrom(self.BUFFER_SIZE)
        except socket.timeout:
            LOG.info('Socket timeout reached, maybe browser service on host: {0} doesnt exist'.format(host))
            sock.close()
            return False

        host.services[self.SERVICE_NAME] = {}

        # Loop through the server data
        instances_list = data[3:].decode().split(';;')
        LOG.info('{0} MSSQL instances found'.format(len(instances_list)))
        for instance in instances_list:
            instance_info = instance.split(';')
            if len(instance_info) > 1:
                host.services[self.SERVICE_NAME][instance_info[1]] = {}
                for i in range(1, len(instance_info), 2):
                    # Each instance's info is nested under its own name, if there are multiple instances
                    # each will appear under its own name
                    host.services[self.SERVICE_NAME][instance_info[1]][instance_info[i - 1]] = instance_info[i]

        # Close the socket
        sock.close()

        return True

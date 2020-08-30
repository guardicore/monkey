import errno
import logging
import socket

import infection_monkey.config
from infection_monkey.network.HostFinger import HostFinger

__author__ = 'Maor Rayzin'

LOG = logging.getLogger(__name__)


class MSSQLFinger(HostFinger):
    # Class related consts
    SQL_BROWSER_DEFAULT_PORT = 1434
    BUFFER_SIZE = 4096
    TIMEOUT = 5
    _SCANNED_SERVICE = 'MSSQL'

    def __init__(self):
        self._config = infection_monkey.config.WormConfiguration

    def get_host_fingerprint(self, host):
        """Gets Microsoft SQL Server instance information by querying the SQL Browser service.
            :arg:
                host (VictimHost): The MS-SSQL Server to query for information.

            :returns:
                Discovered server information written to the Host info struct.
                True if success, False otherwise.
        """

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
        except socket.error as e:
            if e.errno == errno.ECONNRESET:
                LOG.info('Connection was forcibly closed by the remote host. The host: {0} is rejecting the packet.'
                         .format(host))
            else:
                LOG.error('An unknown socket error occurred while trying the mssql fingerprint, closing socket.',
                          exc_info=True)
            sock.close()
            return False

        self.init_service(host.services, self._SCANNED_SERVICE, MSSQLFinger.SQL_BROWSER_DEFAULT_PORT)

        # Loop through the server data
        instances_list = data[3:].decode().split(';;')
        LOG.info('{0} MSSQL instances found'.format(len(instances_list)))
        for instance in instances_list:
            instance_info = instance.split(';')
            if len(instance_info) > 1:
                host.services[self._SCANNED_SERVICE][instance_info[1]] = {}
                for i in range(1, len(instance_info), 2):
                    # Each instance's info is nested under its own name, if there are multiple instances
                    # each will appear under its own name
                    host.services[self._SCANNED_SERVICE][instance_info[1]][instance_info[i - 1]] = instance_info[i]
        # Close the socket
        sock.close()

        return True

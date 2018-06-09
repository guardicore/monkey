import logging
import socket

from model.host import VictimHost
from network import HostFinger
from .tools import struct_unpack_tracker, struct_unpack_tracker_string


LOG = logging.getLogger(__name__)


class MSSQLFingerprint(HostFinger):

    def __init__(self):
        self._config = __import__('config').WormConfiguration

    def get_host_fingerprint(self, host):
        """Gets Microsoft SQL Server instance information by querying the SQL Browser service.
            Args:
                host (str): Hostname or IP address of the SQL Server to query for information.

            Returns:
                Discovered server information written to the Host info struct.
        """

        # Create a UDP socket and sets a timeout
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        server_address = (str(host), browser_port)

        if instance_name:
            # The message is a CLNT_UCAST_INST packet to get a single instance
            # https://msdn.microsoft.com/en-us/library/cc219746.aspx
            message = '\x04{0}\x00'.format(instance_name)
        else:
            # The message is a CLNT_UCAST_EX packet to get all instances
            # https://msdn.microsoft.com/en-us/library/cc219745.aspx
            message = '\x03'

        # Encode the message as a bytesarray
        message = message.encode()

        # send data and receive response
        results = []
        try:
            logging.info('Sending message to requested host: {0}, {1}'.format(host, message))
            sock.sendto(message, server_address)
            data, server = sock.recvfrom(buffer_size)
        except socket.timeout:
            logging.error('Socket timeout reached, maybe browser service on host: {0} doesnt exist'.format(host))
            return results

        # Loop through the server data
        for server in data[3:].decode().split(';;'):
            server_info = OrderedDict()
            instance_info = server.split(';')

            if len(instance_info) > 1:
                for i in range(1, len(instance_info), 2):
                    server_info[instance_info[i - 1]] = instance_info[i]

                results.append(server_info)

        # Close the socket
        sock.close()

        return results

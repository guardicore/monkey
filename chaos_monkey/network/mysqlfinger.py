import socket
import logging
from network import HostFinger
from .tools import struct_unpack_tracker, struct_unpack_tracker_string
from model.host import VictimHost

MYSQL_PORT = 3306
SQL_SERVICE = 'mysqld-3306'

LOG = logging.getLogger(__name__)


class MySQLFinger(HostFinger):
    """
        Fingerprints mysql databases, only on port 3306
    """

    def __init__(self):
        self._config = __import__('config').WormConfiguration

    def get_host_fingerprint(self, host):
        """
        Returns mySQLd data using the host header
        :param host:
        :return: Success/failure, data is saved in the host struct
        """
        assert isinstance(host, VictimHost)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        try:
            s.connect((host.ip_addr, MYSQL_PORT))
            header = s.recv(4)  # max header size?

            tmp, curpos = struct_unpack_tracker(header, 0, "I")
            tmp = tmp[0]
            response_length = tmp & 0xff
            data = s.recv(response_length)
            # now we can start parsing
            protocol, curpos = struct_unpack_tracker(data, 0, "B")
            protocol = protocol[0]

            if protocol == 0xFF:
                # error code, bug out
                LOG.debug("Mysql server returned error")
                return False

            version, curpos = struct_unpack_tracker_string(data, curpos)  # special coded to solve string parsing
            version = version[0]
            host.services[SQL_SERVICE]['version'] = version
            version = version.split('-')[0].split('.')
            host.services[SQL_SERVICE]['major_version'] = version[0]
            host.services[SQL_SERVICE]['minor_version'] = version[1]
            host.services[SQL_SERVICE]['build_version'] = version[2]
            thread_id, curpos = struct_unpack_tracker(data, curpos, "<I")  # ignore thread id

            if protocol == 10:
                # new protocol
                self._parse_protocol_10(curpos, data, host)
                return True
            if protocol == 9:
                return True
            s.close()

        except Exception as err:
            LOG.debug("Error getting mysql fingerprint: %s", err)

        return False

    def _parse_protocol_10(self, curpos, data, host):
        salt, curpos = struct_unpack_tracker(data, curpos, "s8B")
        capabilities, curpos = struct_unpack_tracker(data, curpos, "<H")
        host.services[SQL_SERVICE]['capabilities'] = capabilities[0]
        charset, curpos = struct_unpack_tracker(data, curpos, "B")
        status, curpos = struct_unpack_tracker(data, curpos, "<H")
        extcapabilities, curpos = struct_unpack_tracker(data, curpos, "<H")
        host.services[SQL_SERVICE]['extcapabilities'] = extcapabilities[0]
        # there's more data but it doesn't matter

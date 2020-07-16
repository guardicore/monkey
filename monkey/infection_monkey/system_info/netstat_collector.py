# Inspired by Giampaolo Rodola's psutil example from https://github.com/giampaolo/psutil/blob/master/scripts/netstat.py

import logging
import socket
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM

import psutil

__author__ = 'itay.mizeretz'

LOG = logging.getLogger(__name__)


class NetstatCollector(object):
    """
    Extract netstat info
    """

    AF_INET6 = getattr(socket, 'AF_INET6', object())

    proto_map = {
        (AF_INET, SOCK_STREAM): 'tcp',
        (AF_INET6, SOCK_STREAM): 'tcp6',
        (AF_INET, SOCK_DGRAM): 'udp',
        (AF_INET6, SOCK_DGRAM): 'udp6',
    }

    @staticmethod
    def get_netstat_info():
        LOG.info("Collecting netstat info")
        return [NetstatCollector._parse_connection(c) for c in psutil.net_connections(kind='inet')]

    @staticmethod
    def _parse_connection(c):
        return \
            {
                'proto': NetstatCollector.proto_map[(c.family, c.type)],
                'local_address': c.laddr[0],
                'local_port': c.laddr[1],
                'remote_address': c.raddr[0] if c.raddr else None,
                'remote_port': c.raddr[1] if c.raddr else None,
                'status': c.status,
                'pid': c.pid
            }

import random
import socket
import struct
from abc import ABCMeta, abstractmethod

import ipaddress

from model.host import VictimHost

__author__ = 'itamar'


class NetworkRange(object):
    __metaclass__ = ABCMeta

    def __init__(self, base_address, shuffle=True):
        self._base_address = base_address
        self._shuffle = shuffle
        self._config = __import__('config').WormConfiguration

    @staticmethod
    def _ip_to_number(address):
        return struct.unpack(">L", socket.inet_aton(address))[0]

    @staticmethod
    def _number_to_ip(num):
        return socket.inet_ntoa(struct.pack(">L", num))

    @abstractmethod
    def _get_range(self):
        raise NotImplementedError()

    def __iter__(self):
        base_range = self._get_range()
        if self._shuffle:
            random.shuffle(base_range)

        for x in base_range:
            yield VictimHost(self._number_to_ip(self._base_address + x))


class ClassCRange(NetworkRange):
    def __init__(self, base_address, shuffle=True):
        base_address = struct.unpack(">L", socket.inet_aton(base_address))[0] & 0xFFFFFF00
        super(ClassCRange, self).__init__(base_address, shuffle=shuffle)

    def __repr__(self):
        return "<ClassCRange %s-%s>" % (self._number_to_ip(self._base_address + 1),
                                        self._number_to_ip(self._base_address + 254))

    def _get_range(self):
        return range(1, 254)


class RelativeRange(NetworkRange):
    def __init__(self, base_address, shuffle=True):
        base_address = struct.unpack(">L", socket.inet_aton(base_address))[0]
        super(RelativeRange, self).__init__(base_address, shuffle=shuffle)
        self._size = 1

    def __repr__(self):
        return "<RelativeRange %s-%s>" % (self._number_to_ip(self._base_address - self._size),
                                          self._number_to_ip(self._base_address + self._size))

    def _get_range(self):
        lower_end = -(self._size / 2)
        higher_end = lower_end + self._size
        return range(lower_end, higher_end + 1)


class FixedRange(NetworkRange):
    def __init__(self, fixed_addresses, shuffle=True):
        base_address = 0
        super(FixedRange, self).__init__(base_address, shuffle=shuffle)
        self._fixed_addresses = fixed_addresses

    def __repr__(self):
        return "<FixedRange %s>" % (",".join(self._fixed_addresses))

    @staticmethod
    def _cidr_range_to_ip_list(address_str):
        return [FixedRange._ip_to_number(str(x)) for x in ipaddress.ip_network(unicode(address_str), strict=False)]

    @staticmethod
    def _ip_range_to_ip_list(address_str):
        addresses = address_str.split('-')
        if len(addresses) != 2:
            raise ValueError('Illegal address format: %s' % address_str)
        lower_end, higher_end = [FixedRange._ip_to_number(x.strip()) for x in addresses]
        if higher_end < lower_end:
            raise ValueError('Illegal address range: %s' % address_str)
        return range(lower_end, higher_end + 1)

    @staticmethod
    def _parse_address_str(address_str):
        address_str = address_str.strip()
        if not address_str:  # Empty string
            return []
        if -1 != address_str.find('-'):
            return FixedRange._ip_range_to_ip_list(address_str)
        if -1 != address_str.find('/'):
            return FixedRange._cidr_range_to_ip_list(address_str)
        return [FixedRange._ip_to_number(address_str)]

    def _get_range(self):
        ip_list = list(reduce(
            lambda x, y: x.union(y),
            [set(self._parse_address_str(z)) for z in self._fixed_addresses]))
        return [x for x in ip_list if (x & 0xFF != 0)]  # remove broadcast ips

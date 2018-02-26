import random
import socket
import struct
from abc import ABCMeta, abstractmethod

import ipaddress

__author__ = 'itamar'


class NetworkRange(object):
    __metaclass__ = ABCMeta

    def __init__(self, shuffle=True):
        self._shuffle = shuffle

    def get_range(self):
        return [x for x in self._get_range() if (x & 0xFF != 0)]  # remove broadcast ips

    def __iter__(self):
        base_range = self.get_range()
        if self._shuffle:
            random.shuffle(base_range)

        for x in base_range:
            yield self._number_to_ip(x)

    @abstractmethod
    def is_in_range(self, ip_address):
        raise NotImplementedError()

    @abstractmethod
    def _get_range(self):
        raise NotImplementedError()

    @staticmethod
    def get_range_obj(address_str):
        address_str = address_str.strip()
        if not address_str:  # Empty string
            return None
        if -1 != address_str.find('-'):
            return IpRange(ip_range=address_str)
        if -1 != address_str.find('/'):
            return CidrRange(cidr_range=address_str)
        return SingleIpRange(ip_address=address_str)

    @staticmethod
    def _ip_to_number(address):
        return struct.unpack(">L", socket.inet_aton(address))[0]

    @staticmethod
    def _number_to_ip(num):
        return socket.inet_ntoa(struct.pack(">L", num))


class CidrRange(NetworkRange):
    def __init__(self, cidr_range, shuffle=True):
        super(CidrRange, self).__init__(shuffle=shuffle)
        self._cidr_range = cidr_range.strip()
        self._ip_network = ipaddress.ip_network(unicode(self._cidr_range), strict=False)

    def __repr__(self):
        return "<CidrRange %s>" % (self._cidr_range,)

    def is_in_range(self, ip_address):
        return ipaddress.ip_address(ip_address) in self._ip_network

    def _get_range(self):
        return [CidrRange._ip_to_number(str(x)) for x in self._ip_network]


class IpRange(NetworkRange):
    def __init__(self, ip_range=None, lower_end_ip=None, higher_end_ip=None, shuffle=True):
        super(IpRange, self).__init__(shuffle=shuffle)
        if ip_range is not None:
            addresses = ip_range.split('-')
            if len(addresses) != 2:
                raise ValueError('Illegal IP range format: %s' % ip_range)
            self._lower_end_ip, self._higher_end_ip = [x.strip() for x in addresses]
            if self._higher_end_ip < self._lower_end_ip:
                raise ValueError('Higher end IP is smaller than lower end IP: %s' % ip_range)
        elif (lower_end_ip is not None) and (higher_end_ip is not None):
            self._lower_end_ip = lower_end_ip
            self._higher_end_ip = higher_end_ip
        else:
            raise ValueError('Illegal IP range: %s' % ip_range)

        self._lower_end_ip_num = IpRange._ip_to_number(self._lower_end_ip)
        self._higher_end_ip_num = IpRange._ip_to_number(self._higher_end_ip)

    def __repr__(self):
        return "<IpRange %s-%s>" % (self._lower_end_ip, self._higher_end_ip)

    def is_in_range(self, ip_address):
        return self._lower_end_ip_num <= IpRange._ip_to_number(ip_address) <= self._higher_end_ip_num

    def _get_range(self):
        return range(self._lower_end_ip_num, self._higher_end_ip_num + 1)


class SingleIpRange(NetworkRange):
    def __init__(self, ip_address, shuffle=True):
        super(SingleIpRange, self).__init__(shuffle=shuffle)
        self._ip_address = ip_address

    def __repr__(self):
        return "<SingleIpRange %s>" % (self._ip_address,)

    def is_in_range(self, ip_address):
        return self._ip_address == ip_address

    def _get_range(self):
        return [SingleIpRange._ip_to_number(self._ip_address)]

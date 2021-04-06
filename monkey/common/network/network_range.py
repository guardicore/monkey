import ipaddress
import logging
import random
import socket
import struct
from abc import ABCMeta, abstractmethod

__author__ = 'itamar'

LOG = logging.getLogger(__name__)


class NetworkRange(object, metaclass=ABCMeta):
    def __init__(self, shuffle=True):
        self._shuffle = shuffle

    def get_range(self):
        """
        :return: Returns a sequence of IPs in an internal format (might be numbers)
        """
        return self._get_range()

    def __iter__(self):
        """
        Iterator of ip addresses (strings) from the current range.
        Use get_range if you want it in one go.
        :return:
        """
        base_range = self.get_range()
        if self._shuffle:
            random.shuffle(base_range)  # noqa: DUO102

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
        if not address_str:  # Empty string
            return None
        address_str = address_str.strip()
        if NetworkRange.check_if_range(address_str):
            return IpRange(ip_range=address_str)
        if -1 != address_str.find('/'):
            return CidrRange(cidr_range=address_str)
        return SingleIpRange(ip_address=address_str)

    @staticmethod
    def check_if_range(address_str):
        if -1 != address_str.find('-'):
            ips = address_str.split('-')
            try:
                ipaddress.ip_address(ips[0]) and ipaddress.ip_address(ips[1])
            except ValueError:
                return False
            return True
        return False

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
        self._ip_network = ipaddress.ip_network(str(self._cidr_range), strict=False)

    def __repr__(self):
        return "<CidrRange %s>" % (self._cidr_range,)

    def is_in_range(self, ip_address):
        return ipaddress.ip_address(ip_address) in self._ip_network

    def _get_range(self):
        return [CidrRange._ip_to_number(str(x)) for x in self._ip_network if x != self._ip_network.broadcast_address]


class IpRange(NetworkRange):
    def __init__(self, ip_range=None, lower_end_ip=None, higher_end_ip=None, shuffle=True):
        super(IpRange, self).__init__(shuffle=shuffle)
        if ip_range is not None:
            addresses = ip_range.split('-')
            if len(addresses) != 2:
                raise ValueError('Illegal IP range format: %s. Format is 192.168.0.5-192.168.0.20' % ip_range)
            self._lower_end_ip, self._higher_end_ip = [x.strip() for x in addresses]
        elif (lower_end_ip is not None) and (higher_end_ip is not None):
            self._lower_end_ip = lower_end_ip.strip()
            self._higher_end_ip = higher_end_ip.strip()
        else:
            raise ValueError('Illegal IP range: %s' % ip_range)

        self._lower_end_ip_num = self._ip_to_number(self._lower_end_ip)
        self._higher_end_ip_num = self._ip_to_number(self._higher_end_ip)
        if self._higher_end_ip_num < self._lower_end_ip_num:
            raise ValueError(
                'Higher end IP %s is smaller than lower end IP %s' % (self._lower_end_ip, self._higher_end_ip))

    def __repr__(self):
        return "<IpRange %s-%s>" % (self._lower_end_ip, self._higher_end_ip)

    def is_in_range(self, ip_address):
        return self._lower_end_ip_num <= self._ip_to_number(ip_address) <= self._higher_end_ip_num

    def _get_range(self):
        return list(range(self._lower_end_ip_num, self._higher_end_ip_num + 1))


class SingleIpRange(NetworkRange):
    def __init__(self, ip_address, shuffle=True):
        super(SingleIpRange, self).__init__(shuffle=shuffle)
        self._ip_address, self.domain_name = self.string_to_host(ip_address)

    def __repr__(self):
        return "<SingleIpRange %s>" % (self._ip_address,)

    def __iter__(self):
        """
        We have to check if we have an IP to return, because user could have entered invalid
        domain name and no IP was found
        :return: IP if there is one
        """
        if self.ip_found():
            yield self._number_to_ip(self.get_range()[0])

    def is_in_range(self, ip_address):
        return self._ip_address == ip_address

    def _get_range(self):
        return [SingleIpRange._ip_to_number(self._ip_address)]

    def ip_found(self):
        """
        Checks if we could translate domain name entered into IP address
        :return: True if dns found domain name and false otherwise
        """
        return self._ip_address

    @staticmethod
    def string_to_host(string_):
        """
        Converts the string that user entered in "Scan IP/subnet list" to a tuple of domain name and ip
        :param string_: String that was entered in "Scan IP/subnet list"
        :return: A tuple in format (IP, domain_name). Eg. (192.168.55.1, www.google.com)
        """
        # The most common use case is to enter ip/range into "Scan IP/subnet list"
        domain_name = ''

        # Try casting user's input as IP
        try:
            ip = ipaddress.ip_address(string_).exploded
        except ValueError:
            # Exception means that it's a domain name
            try:
                ip = socket.gethostbyname(string_)
                domain_name = string_
            except socket.error:
                LOG.error("Your specified host: {} is not found as a domain name and"
                          " it's not an IP address".format(string_))
                return None, string_
        # If a string_ was entered instead of IP we presume that it was domain name and translate it
        return ip, domain_name

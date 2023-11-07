import ipaddress
import logging
import random
import re
import socket
import struct
from abc import ABCMeta, abstractmethod
from typing import Iterable, List, Tuple

logger = logging.getLogger(__name__)


class InvalidNetworkRangeError(Exception):
    """Raise when invalid network range is provided"""


class NetworkRange(object, metaclass=ABCMeta):
    DOMAIN_LABEL_PATTERN = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
    TLD_PATTERN = re.compile(r"[0-9]+$")

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
        if address_str.endswith("/32"):
            address_str = address_str[:-3]
        if NetworkRange.check_if_hostname(address_str):
            return SingleIpRange(ip_address=address_str)
        if NetworkRange.check_if_range(address_str):
            return IpRange(ip_range=address_str)
        if "/" in address_str:
            return CidrRange(cidr_range=address_str)
        return SingleIpRange(ip_address=address_str)

    @staticmethod
    def filter_invalid_ranges(ranges: Iterable[str], error_msg: str) -> List[str]:
        valid_ranges = []
        for target_range in ranges:
            try:
                NetworkRange.validate_range(target_range)
            except InvalidNetworkRangeError as e:
                logger.error(f"{error_msg} {e}")
                continue
            valid_ranges.append(target_range)
        return valid_ranges

    @staticmethod
    def validate_range(address_str: str):
        try:
            NetworkRange.get_range_obj(address_str)
        except (ValueError, OSError) as e:
            raise InvalidNetworkRangeError(e)

    @staticmethod
    def check_if_hostname(hostname: str):
        if len(hostname) > 253 or hostname[-1] == ".":
            return False

        labels = hostname.split(".")

        # the TLD must be not all-numeric
        if NetworkRange.TLD_PATTERN.match(labels[-1]):
            return False

        return all([NetworkRange.DOMAIN_LABEL_PATTERN.match(label) for label in labels])

    @staticmethod
    def check_if_range(address_str: str):
        if -1 != address_str.find("-"):
            try:
                NetworkRange._range_to_ips(address_str)
            except ValueError:
                return False
            return True
        return False

    @staticmethod
    def _range_to_ips(ip_range: str) -> Tuple[str, str]:
        ips = ip_range.split("-")
        ips = [ip.strip() for ip in ips]
        ips = sorted(ips, key=lambda ip: socket.inet_aton(ip))
        return ips[0], ips[1]

    @staticmethod
    def _ip_to_number(address):
        return struct.unpack(">L", socket.inet_aton(str(address)))[0]

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
        return [
            CidrRange._ip_to_number(str(x))
            for x in self._ip_network
            if x != self._ip_network.broadcast_address
        ]


class IpRange(NetworkRange):
    def __init__(self, ip_range=None, lower_end_ip=None, higher_end_ip=None, shuffle=True):
        super(IpRange, self).__init__(shuffle=shuffle)
        if ip_range is not None:
            self._lower_end_ip, self._higher_end_ip = IpRange._range_to_ips(ip_range)
        elif (lower_end_ip is not None) and (higher_end_ip is not None):
            self._lower_end_ip = lower_end_ip.strip()
            self._higher_end_ip = higher_end_ip.strip()
        else:
            raise ValueError("Illegal IP range: %s" % ip_range)

        self._lower_end_ip_num = self._ip_to_number(self._lower_end_ip)
        self._higher_end_ip_num = self._ip_to_number(self._higher_end_ip)
        if self._higher_end_ip_num < self._lower_end_ip_num:
            raise ValueError(
                "Higher end IP %s is smaller than lower end IP %s"
                % (self._lower_end_ip, self._higher_end_ip)
            )

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
        return self._ip_address == str(ip_address)

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
        Converts the string that user entered in "Scan IP/subnet list" to a tuple of domain name
        and ip

        :param string_: String that was entered in "Scan IP/subnet list"
        :return: A tuple in format (IP, domain_name). Eg. (192.168.55.1, www.google.com)
        """
        # The most common use case is to enter ip/range into "Scan IP/subnet list"
        domain_name = None

        if " " in string_:
            raise ValueError(f'"{string_}" is not a valid IP address or domain name.')

        # Try casting user's input as IP
        try:
            ip = ipaddress.ip_address(string_).exploded
        except ValueError:
            # Exception means that it's a domain name
            try:
                ip = socket.gethostbyname(string_)
                domain_name = string_
            except socket.error:
                raise ValueError(
                    "Your specified host: {} is not found as a domain name and"
                    " it's not an IP address".format(string_)
                )
        # If a string_ was entered instead of IP we presume that it was domain name and translate it
        return ip, domain_name

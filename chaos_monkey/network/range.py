
import socket
import random
import struct
from abc import ABCMeta, abstractmethod
from model.host import VictimHost

__author__ = 'itamar'

class NetworkRange(object):
    __metaclass__ = ABCMeta

    def __init__(self, base_address, shuffle=True):
        self._base_address = base_address
        self._shuffle = shuffle
        self._config = __import__('config').WormConfiguration

    @abstractmethod
    def _get_range(self):
        raise NotImplementedError()

    def __iter__(self):
        base_range = self._get_range()
        if self._shuffle:
            random.shuffle(base_range)

        for x in base_range:
            yield VictimHost(socket.inet_ntoa(struct.pack(">L", self._base_address + x)))


class ClassCRange(NetworkRange):
    def __init__(self, base_address, shuffle=True):
        base_address = struct.unpack(">L", socket.inet_aton(base_address))[0] & 0xFFFFFF00
        super(ClassCRange, self).__init__(base_address, shuffle=shuffle)

    def __repr__(self):
        return "<ClassCRange %s-%s>" % (socket.inet_ntoa(struct.pack(">L", self._base_address + 1)),
                                         socket.inet_ntoa(struct.pack(">L", self._base_address + 254)))

    def _get_range(self):
        return range(1, 254)


class RelativeRange(NetworkRange):
    def __init__(self, base_address, shuffle=True):
        base_address = struct.unpack(">L", socket.inet_aton(base_address))[0]
        super(RelativeRange, self).__init__(base_address, shuffle=shuffle)
        self._size = self._config.range_size

    def __repr__(self):
        return "<RelativeRange %s-%s>" % (socket.inet_ntoa(struct.pack(">L", self._base_address - self._size)),
                                         socket.inet_ntoa(struct.pack(">L", self._base_address + self._size)))

    def _get_range(self):
        return range(-self._size, self._size + 1)


class FixedRange(NetworkRange):
    def __init__(self, base_address, shuffle=True):
        base_address = 0
        super(FixedRange, self).__init__(base_address, shuffle=shuffle)
        self._fixed_addresses = self._config.range_fixed

    def __repr__(self):
        return "<FixedRange %s>" % (",".join(self._fixed_addresses))

    def _get_range(self):
        return [struct.unpack(">L", socket.inet_aton(address))[0]
                for address in self._fixed_addresses]
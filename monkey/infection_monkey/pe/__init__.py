from abc import ABCMeta, abstractmethod

__author__ = 'D3fa1t'

class HostPrivExploiter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def try_priv_esc(self,commad):
        raise NotImplementedError()

from .snapd import snapdExploiter

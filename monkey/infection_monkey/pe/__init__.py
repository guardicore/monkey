from abc import ABCMeta, abstractmethod

__author__ = 'D3fa1t'

class HostPrivExploiter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def try_priv_esc(self,commad):
        raise NotImplementedError()

    def send_pe_telemetry(self, result, local_ip):
        from infection_monkey.control import ControlClient
        ControlClient.send_telemetry('pe', {'result': result, 'pe_name': self.__class__.__name__, 'ip': local_ip})

from infection_monkey.pe.snapd import snapdExploiter


from abc import ABCMeta, abstractmethod

__author__ = 'itamar'

class MonitorCondition(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def check_condition(self):
        raise NotImplementedError()

from files import FilesExistCondition
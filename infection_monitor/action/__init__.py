
from abc import ABCMeta, abstractmethod

__author__ = 'itamar'

class MonitorAction(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def do_action(self):
        raise NotImplementedError()

    @abstractmethod
    def undo_action(self):
        raise NotImplementedError()

from desktop import ChangeDesktopAction

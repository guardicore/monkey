from abc import ABCMeta, abstractmethod

from envs.monkey_zoo.blackbox.tests.basic_test import BasicTest


class PerformanceTest(BasicTest, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, island_client, raw_config, analyzers,
                 timeout, log_handler, break_on_timeout):
        pass

    @property
    @abstractmethod
    def TEST_NAME(self):
        pass

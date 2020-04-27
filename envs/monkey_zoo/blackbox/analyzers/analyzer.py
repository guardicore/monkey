from abc import ABCMeta, abstractmethod


class Analyzer(object, metaclass=ABCMeta):

    @abstractmethod
    def analyze_test_results(self):
        raise NotImplementedError()

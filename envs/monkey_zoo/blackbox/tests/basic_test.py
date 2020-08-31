import abc


class BasicTest(abc.ABC):

    @abc.abstractmethod
    def run(self):
        pass

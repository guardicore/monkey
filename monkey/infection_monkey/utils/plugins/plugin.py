from abc import ABCMeta, abstractmethod


class Plugin(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def should_run(class_name: str) -> bool:
        raise NotImplementedError()

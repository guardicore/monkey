from abc import ABC, abstractmethod


class ConfigTemplate(ABC):

    @property
    @abstractmethod
    def config_values(self) -> dict:
        pass

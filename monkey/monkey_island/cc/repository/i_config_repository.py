from abc import ABC

from common.configuration import AgentConfiguration


class IConfigRepository(ABC):
    def get_config(self) -> AgentConfiguration:
        pass

    def set_config(self, config: AgentConfiguration):
        pass

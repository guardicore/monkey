from abc import ABC, abstractmethod

from agentpluginapi import AgentBinaryTransform


class Transformer(ABC):
    @abstractmethod
    def transform(self) -> AgentBinaryTransform:
        pass

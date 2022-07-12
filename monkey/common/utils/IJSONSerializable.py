from __future__ import annotations

from abc import ABC, abstractmethod


class IJSONSerializable(ABC):
    @classmethod
    @abstractmethod
    def from_json(cls, json_string: str) -> IJSONSerializable:
        pass

    @classmethod
    @abstractmethod
    def to_json(cls, class_object: IJSONSerializable) -> str:
        pass

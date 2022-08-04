from typing import Any, Sequence, Type, TypeVar
from unittest.mock import MagicMock

from common import DIContainer, UnregisteredTypeError

T = TypeVar("T")


class StubDIContainer(DIContainer):
    def __init__(self):
        super().__init__()
        self._convention_registry[(Sequence[str], "local_ip_addresses")] = []

    def resolve(self, type_: Type[T]) -> T:
        try:
            return super().resolve(type_)
        except UnregisteredTypeError:
            return MagicMock()

    def resolve_dependencies(self, type_: Type[T]) -> Sequence[Any]:
        try:
            return super().resolve_dependencies(type_)
        except UnregisteredTypeError:
            return MagicMock()

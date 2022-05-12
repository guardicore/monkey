from typing import Any, Sequence, Type, TypeVar
from unittest.mock import MagicMock

from common import DIContainer, UnregisteredTypeError

T = TypeVar("T")


class StubDIContainer(DIContainer):
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

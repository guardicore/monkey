from types import TracebackType
from typing import Optional, Protocol, Type


class BasicLock(Protocol):
    def __enter__(self) -> bool:
        ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        ...

    def acquire(self, blocking: bool = ..., timeout: float = ...) -> bool:
        ...

    def release(self) -> None:
        ...


class Lock(BasicLock, Protocol):
    def locked(self) -> bool:
        ...


class RLock(BasicLock, Protocol):
    def __enter__(self, blocking: bool = ..., timeout: float = ...) -> bool:
        ...


class Event(Protocol):
    def is_set(self) -> bool:
        ...

    def set(self) -> None:
        ...

    def clear(self) -> None:
        ...

    def wait(self, timeout: Optional[float] = ...) -> bool:
        ...

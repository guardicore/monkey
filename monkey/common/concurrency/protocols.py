from types import TracebackType
from typing import Optional, Protocol, Type


class Lock(Protocol):
    def __enter__(self) -> bool:
        ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        ...

    def acquire(self, blocking: bool = ..., timeout: float = ...) -> bool:
        ...

    def release(self) -> None:
        ...

    def locked(self) -> bool:
        ...

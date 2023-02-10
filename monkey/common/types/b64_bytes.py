from base64 import b64decode
from typing import Any, Callable, Generator

from pydantic import errors


def b64_bytes_validator(val: Any) -> bytes:
    if isinstance(val, bytes):
        return val
    elif isinstance(val, bytearray):
        return bytes(val)
    elif isinstance(val, str):
        try:
            return b64decode(val)
        except Exception as e:
            new_error = errors.BytesError()
            new_error.msg_template = "Failed to decode b64 string to bytes"
            raise new_error from e
    raise errors.BytesError()


class B64Bytes(bytes):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield b64_bytes_validator

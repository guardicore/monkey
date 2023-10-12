from pathlib import PurePath, PurePosixPath, PureWindowsPath
from typing import Any, Dict, Mapping, Tuple

from monkeytypes import OperatingSystem
from pydantic import ConfigDict, Field, field_serializer, field_validator

from . import AbstractAgentEvent


def _serialize_pure_path(pure_path: PurePath) -> Dict[str, str]:
    # We generate data on either Windows or Linux and that data is processed
    # on either OS which we can't sure where, so be need to serialize it as
    # dictionary containing the path as string and the operating system
    # which depends of the type of the path
    serialized_os = (
        OperatingSystem.LINUX.value
        if isinstance(pure_path, PurePosixPath)
        else OperatingSystem.WINDOWS.value
    )
    return {"path": str(pure_path), "os": serialized_os}


class FileEncryptionEvent(AbstractAgentEvent):
    """
    An event that occurs when the Agent encrypts a file

    Attributes:
        :param file_path: Path of the encrypted file
        :param success: Status of the file encryption
        :param error_message: Message if an error occurs during file encryption
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    file_path: PurePath
    success: bool
    error_message: str = Field(default="")

    @field_serializer("file_path", when_used="json")
    def dump_file_path(self, v):
        return _serialize_pure_path(v)

    @field_validator("file_path", mode="before")
    @classmethod
    def _file_path_to_pure_path(cls, v: Any) -> PurePath:
        if isinstance(v, PurePath):
            return v

        if not isinstance(v, Mapping):
            raise TypeError(f"Expected mapping but got {type(v)}")

        path_string, os_string = FileEncryptionEvent._parse_path_dict(v)

        if not isinstance(os_string, str):
            raise TypeError("Operating system must be a string")

        if os_string == OperatingSystem.LINUX.value:
            return PurePosixPath(path_string)
        elif os_string == OperatingSystem.WINDOWS.value:
            return PureWindowsPath(path_string)

        raise ValueError(f'"{os_string}" is not a valid operating system')

    @staticmethod
    def _parse_path_dict(path_dict: Mapping[str, str]) -> Tuple[str, str]:
        try:
            path_string = path_dict["path"]
            os_string = path_dict["os"]
        except KeyError as err:
            raise ValueError(f'Missing key "{err}" in pure path dictionary')

        return path_string, os_string

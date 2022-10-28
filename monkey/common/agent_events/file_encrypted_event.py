from pathlib import PurePath

from pydantic import Field

from . import AbstractAgentEvent


class FileEncryptedEvent(AbstractAgentEvent):
    """
    An event that occurs when the Agent encrypts a file.

    Attributes:
        :param file_path: Path of the encrypted file
        :param success: Status of the file encryption
        :param error_message: Message if an error occurs during file encryption
    """

    file_path: PurePath
    success: bool
    error_message: str = Field(default="")

    class Config:
        arbitrary_types_allowed = True

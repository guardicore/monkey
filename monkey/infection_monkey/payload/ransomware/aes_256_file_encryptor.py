from pathlib import Path
from typing import Literal, Union

import pyAesCrypt

from common.types import FileExtension

TMP_EXTENSION = ".tmp"


# TODO: Consider using the cryptography library with CTR mode instead of pyAesCrypt
class AES256FileEncryptor:
    def __init__(self, password: str, new_file_extension: Union[Literal[""], FileExtension] = ""):
        self._password = password
        self._new_file_extension = new_file_extension

    def __call__(self, filepath: Path):
        if self._new_file_extension:
            src_path = filepath
            dst_path = Path(str(src_path) + self._new_file_extension)
        else:
            src_path = filepath.with_suffix(TMP_EXTENSION)
            filepath.rename(src_path)
            dst_path = filepath

        pyAesCrypt.encryptFile(src_path, dst_path, self._password)
        src_path.unlink()

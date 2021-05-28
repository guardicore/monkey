import logging
import os
from typing import Optional, Tuple

import pyAesCrypt

logger = logging.getLogger(__name__)


def encrypt_file_with_password(
    plaintext_file_path: str,
    encrypted_file_path: str,
    password: str,
    should_remove_plaintext_file: bool = True,
) -> Tuple[bool, Optional[bool]]:

    file_encryption_successful = False
    try:
        pyAesCrypt.encryptFile(plaintext_file_path, encrypted_file_path, password)
        file_encryption_successful = True
    except Exception as ex:
        logger.error(f"Could not encrypt config file: {str(ex)}")

    plaintext_file_removal_successful = False
    if file_encryption_successful and should_remove_plaintext_file:
        plaintext_file_removal_successful = remove_file(plaintext_file_path)

    return file_encryption_successful, plaintext_file_removal_successful


def remove_file(path: str) -> bool:
    file_removal_successful = False
    try:
        os.remove_file(path)
        file_removal_successful = True
    except Exception as ex:
        logger.error(f"Could not remove plaintext file: {str(ex)}")

    return file_removal_successful

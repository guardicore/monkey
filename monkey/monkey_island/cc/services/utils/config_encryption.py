import io
import json
from typing import Dict

import pyAesCrypt

from common.utils.exceptions import FailedDecryption, NoCredentialsError

# TODO use from pyAesCrypt
BUFFER_SIZE = 64 * 1024


def encrypt_config(config: Dict, password: str) -> str:
    plaintext_config_stream = io.BytesIO(json.dumps(config).encode())
    ciphertext_config_stream = io.BytesIO()

    pyAesCrypt.encryptStream(
        plaintext_config_stream, ciphertext_config_stream, password, BUFFER_SIZE
    )

    ciphertext_config_bytes = str(ciphertext_config_stream.getvalue())
    return ciphertext_config_bytes


def decrypt_config(enc_config: bytes, password: str) -> Dict:
    if not password:
        raise NoCredentialsError

    ciphertext_config_stream = io.BytesIO(enc_config)
    dec_plaintext_config_stream = io.BytesIO()

    len_ciphertext_config_stream = len(ciphertext_config_stream.getvalue())

    try:
        pyAesCrypt.decryptStream(
            ciphertext_config_stream,
            dec_plaintext_config_stream,
            password,
            BUFFER_SIZE,
            len_ciphertext_config_stream,
        )
    except ValueError as ex:
        raise FailedDecryption(str(ex))

    plaintext_config = json.loads(dec_plaintext_config_stream.getvalue().decode("utf-8"))
    return plaintext_config

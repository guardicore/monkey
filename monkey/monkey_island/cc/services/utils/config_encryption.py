import base64
import io
import json
from typing import Dict

import pyAesCrypt

from common.utils.exceptions import FailedDecryption, NoCredentialsError

BUFFER_SIZE = pyAesCrypt.crypto.bufferSizeDef


def encrypt_config(config: Dict, password: str) -> str:
    plaintext_config_stream = io.BytesIO(json.dumps(config).encode())
    ciphertext_config_stream = io.BytesIO()

    pyAesCrypt.encryptStream(
        plaintext_config_stream, ciphertext_config_stream, password, BUFFER_SIZE
    )

    ciphertext_b64 = base64.b64encode(ciphertext_config_stream.getvalue())

    return ciphertext_b64.decode()


def decrypt_config(cyphertext: str, password: str) -> Dict:
    if not password:
        raise NoCredentialsError

    cyphertext = base64.b64decode(cyphertext)

    ciphertext_config_stream = io.BytesIO(cyphertext)
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

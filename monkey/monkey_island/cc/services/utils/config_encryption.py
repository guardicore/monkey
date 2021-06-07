import base64
import io
import json
import logging
from typing import Dict

import pyAesCrypt

from common.utils.exceptions import InvalidCredentialsError, NoCredentialsError

BUFFER_SIZE = pyAesCrypt.crypto.bufferSizeDef

logger = logging.getLogger(__name__)


def encrypt_config(config: Dict, password: str) -> str:
    plaintext_config_stream = io.BytesIO(json.dumps(config).encode())
    ciphertext_config_stream = io.BytesIO()

    pyAesCrypt.encryptStream(
        plaintext_config_stream, ciphertext_config_stream, password, BUFFER_SIZE
    )

    ciphertext_b64 = base64.b64encode(ciphertext_config_stream.getvalue())
    logger.info("Configuration encrypted.")

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
        if str(ex).startswith("Wrong password"):
            logger.info("Wrong password for configuration provided.")
            raise InvalidCredentialsError
        else:
            logger.info("The provided configuration file is corrupt.")
            raise ex
    plaintext_config = json.loads(dec_plaintext_config_stream.getvalue().decode("utf-8"))
    return plaintext_config

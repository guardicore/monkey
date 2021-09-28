import logging

from monkey_island.cc.server_utils.encryption import get_datastore_encryptor
from monkey_island.cc.server_utils.encryption.dict_encryption.field_encryptors import (
    IFieldEncryptor,
)

logger = logging.getLogger(__name__)


class MimikatzResultsEncryptor(IFieldEncryptor):

    secret_types = ["password", "ntlm_hash", "lm_hash"]

    @staticmethod
    def encrypt(results: dict) -> dict:
        for _, credentials in results.items():
            for secret_type in MimikatzResultsEncryptor.secret_types:
                try:
                    credentials[secret_type] = get_datastore_encryptor().enc(
                        credentials[secret_type]
                    )
                except ValueError as e:
                    logger.error(
                        f"Failed encrypting sensitive field for "
                        f"user {credentials['username']}! Error: {e}"
                    )
                    credentials[secret_type] = get_datastore_encryptor().enc("")
        return results

    @staticmethod
    def decrypt(results: dict) -> dict:
        for _, credentials in results.items():
            for secret_type in MimikatzResultsEncryptor.secret_types:
                credentials[secret_type] = get_datastore_encryptor().dec(credentials[secret_type])
        return results

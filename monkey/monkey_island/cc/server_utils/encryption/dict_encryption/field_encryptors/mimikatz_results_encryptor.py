import logging

from ... import get_datastore_encryptor
from . import IFieldEncryptor

logger = logging.getLogger(__name__)


class MimikatzResultsEncryptor(IFieldEncryptor):

    secret_types = ["password", "ntlm_hash", "lm_hash"]

    @staticmethod
    def encrypt(results: dict) -> dict:
        for _, credentials in results.items():
            for secret_type in MimikatzResultsEncryptor.secret_types:
                credentials[secret_type] = get_datastore_encryptor().encrypt(
                    credentials[secret_type]
                )
        return results

    @staticmethod
    def decrypt(results: dict) -> dict:
        for _, credentials in results.items():
            for secret_type in MimikatzResultsEncryptor.secret_types:
                credentials[secret_type] = get_datastore_encryptor().decrypt(
                    credentials[secret_type]
                )
        return results

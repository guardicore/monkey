from monkey_island.cc.models.utils.field_encryptors.i_field_encryptor import IFieldEncryptor
from monkey_island.cc.server_utils.encryptor import get_encryptor


class MimikatzResultsEncryptor(IFieldEncryptor):

    secret_types = ["password", "ntlm_hash", "lm_hash"]

    @staticmethod
    def encrypt(results: dict) -> dict:
        for _, credentials in results.items():
            for secret_type in MimikatzResultsEncryptor.secret_types:
                credentials[secret_type] = get_encryptor().enc(credentials[secret_type])
        return results

    @staticmethod
    def decrypt(results: dict) -> dict:
        for _, credentials in results.items():
            for secret_type in MimikatzResultsEncryptor.secret_types:
                credentials[secret_type] = get_encryptor().dec(credentials[secret_type])
        return results

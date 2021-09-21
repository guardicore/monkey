from monkey_island.cc.server_utils.encryptor import get_encryptor


def encrypt(cleartext: str) -> str:
    return get_encryptor().enc(cleartext)


def decrypt(cyphertext: str) -> str:
    return get_encryptor().dec(cyphertext)

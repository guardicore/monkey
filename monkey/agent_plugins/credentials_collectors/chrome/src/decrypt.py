# TODO: See if another module can replace this one
from Crypto.Cipher import AES

from .aes import AESModeOfOperationCBC


def decrypt_AES(
    encrypted_value: bytes, decryption_key: bytes, init_vector: bytes, block_size: int
) -> str:
    encrypted_value = encrypted_value[3:]
    aes = AESModeOfOperationCBC(decryption_key, iv=init_vector)
    cleartxt = b"".join(
        [
            aes.decrypt(encrypted_value[i : i + block_size])
            for i in range(0, len(encrypted_value), block_size)
        ]
    )
    return _remove_padding(cleartxt).decode()


def _remove_padding(data: bytes) -> bytes:
    """
    Remove PKCS#7 padding
    """
    nb = data[-1]

    try:
        return data[:-nb]
    except Exception:
        return data


def decrypt_v80(buff, master_key) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16]  # .decode()  # remove suffix bytes
    return decrypted_pass.decode()

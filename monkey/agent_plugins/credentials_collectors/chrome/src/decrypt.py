from Cryptodome.Cipher import AES

AES_BLOCK_SIZE = 16  # AES uses a fixed block size of 16 bytes


def decrypt_AES(encrypted_value: bytes, decryption_key: bytes, init_vector: bytes) -> str:
    """
    Decrypts a password encrypted with AES

    :param encrypted_value: The password to decrypt
    :param decryption_key: The key to use for decryption
    :param init_vector: The initialization vector to use for decryption
    :return: The decrypted password string
    :raises UnicodeDecodeError: If the password cannot be decoded to a string
    :raises ValueError: If the password cannot be decrypted
    """
    encrypted_value = encrypted_value[3:]
    aes = AES.new(decryption_key, AES.MODE_CBC, iv=init_vector)
    cleartxt = b"".join(
        [
            aes.decrypt(encrypted_value[i : i + AES_BLOCK_SIZE])
            for i in range(0, len(encrypted_value), AES_BLOCK_SIZE)
        ]
    )
    return _remove_padding(cleartxt).decode()


def _remove_padding(data: bytes) -> bytes:
    """
    Remove PKCS#7 padding
    """
    nb = data[-1]
    if len(data) < nb:
        raise ValueError("PKCS#7 padding is incorrect.")
    return data[:-nb]


def decrypt_v80(encrypted_password: bytes, decryption_key: bytes) -> str:
    """
    Decrypts a password encrypted with the v80 Chrome encryption scheme

    :param encrypted_password: The password to decrypt
    :param decryption_key: The key to use for decryption
    :return: The decrypted password string
    :raises UnicodeDecodeError: If the password cannot be decoded to a string
    :raises ValueError: If the password cannot be decrypted
    """
    iv = encrypted_password[3:15]
    payload = encrypted_password[15:]
    cipher = AES.new(decryption_key, AES.MODE_GCM, iv)

    decrypted_pass = cipher.decrypt(payload)
    if len(decrypted_pass) <= 16:
        raise ValueError("Failed to decrypt password")
    decrypted_pass = decrypted_pass[:-16]  # remove suffix bytes

    return decrypted_pass.decode()

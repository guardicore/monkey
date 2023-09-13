from Cryptodome.Cipher import AES


def decrypt_AES(
    encrypted_value: bytes, decryption_key: bytes, init_vector: bytes, block_size: int
) -> str:
    """
    :raises UnicodeDecodeError: If the password cannot be decoded to a string
    :raises ValueError: If the password cannot be decrypted
    """
    encrypted_value = encrypted_value[3:]
    aes = AES.new(decryption_key, AES.MODE_CBC, iv=init_vector)
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
    if len(data) < nb:
        raise ValueError("PKCS#7 padding is incorrect.")
    return data[:-nb]


def decrypt_v80(buff, master_key) -> str:
    """
    :raises UnicodeDecodeError: If the password cannot be decoded to a string
    :raises ValueError: If the password cannot be decrypted
    """
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    if len(decrypted_pass) <= 16:
        raise ValueError("Failed to decrypt password")
    decrypted_pass = decrypted_pass[:-16]  # remove suffix bytes

    return decrypted_pass.decode()

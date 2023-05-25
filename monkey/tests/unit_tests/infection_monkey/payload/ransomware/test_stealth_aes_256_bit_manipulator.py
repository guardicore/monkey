import pyaes
import pytest

from infection_monkey.payload.ransomware.stealth_aes_256_bit_manipulator import (
    StealthAES256BitManipulator,
)

key = b"a" * 32


@pytest.mark.slow
@pytest.mark.parametrize(
    "plaintext",
    [
        b"a" * 1,
        b"b" * 8,
        b"c" * 16,
        b"d" * 32,
        b"e" * 64,
        b"f" * 128,
        b"g" * 17,
        b"h" * 23,
        b"i" * 273,
        b"j" * 17319,
    ],
    ids=["a1", "b8", "c16", "d32", "e64", "f128", "g17", "h23", "i273", "j17319"],
)
def test_encryption(plaintext: bytes):
    decryptor = pyaes.AESModeOfOperationCTR(key)
    bit_manipulator = StealthAES256BitManipulator(key)

    cyphertext = bit_manipulator(plaintext)
    decrypted = decryptor.decrypt(cyphertext)

    assert cyphertext != plaintext
    assert decrypted == plaintext

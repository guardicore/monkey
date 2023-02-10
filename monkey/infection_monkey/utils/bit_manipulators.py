from typing import Iterable


def generate_flipped_bits(data: bytes) -> Iterable[int]:
    """
    Yield bytes with the bits flipped

    :param data: The data whose bits to flip
    """
    for byte in data:
        yield 255 - byte


def flip_bits(data: bytes) -> bytes:
    """
    Flip all bits in the given bytes

    :param data: The bytes whose bits to flip
    :return: Bytes with the bits flipped
    """
    return bytes(generate_flipped_bits(data))

def flip_bits(data: bytes) -> bytes:
    flipped_bits = bytearray(len(data))

    for i, byte in enumerate(data):
        flipped_bits[i] = flip_bits_in_single_byte(byte)

    return bytes(flipped_bits)


def flip_bits_in_single_byte(byte) -> int:
    return 255 ^ byte

def flip_bits(data: bytes) -> bytes:
    flipped_bits = bytearray(len(data))

    for i, byte in enumerate(data):
        # TODO: The function call to flip_bits_in_single_byte() adds significant
        #       overhead. While python is supposed to "inline" function calls
        #       like this, I've yet to see any changes in runtime that indicate
        #       this optimization is actually happening.
        #
        #       The value of breaking this into separate functions is the unit
        #       test that tests all possible bytes (0-255). This gives us
        #       confidence that our bit-flip operation is correct.
        #
        #       Remove the flip_bits_in_single_byte() function and rework the
        #       unit tests so that we still have a high-degree of confidence
        #       that this code is correct.
        #
        #       EDIT: I believe PyPy will attempt to inline functions
        #       automatically. I don't know that CPython makes any such
        #       optimizations.
        flipped_bits[i] = flip_bits_in_single_byte(byte)

    return bytes(flipped_bits)


def flip_bits_in_single_byte(byte) -> int:
    # TODO: The operation `255 - byte` appears to be 12% faster than 255 ^ byte.
    #       Switch the operator and thoroughly test the ransomware payload to
    #       ensure this doesn't introduce any defects.
    return 255 ^ byte

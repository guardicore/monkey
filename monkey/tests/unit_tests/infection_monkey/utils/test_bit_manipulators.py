from infection_monkey.utils import bit_manipulators


def test_flip_bits_in_single_byte():
    for i in range(0, 256):
        assert bit_manipulators.flip_bits_in_single_byte(i) == (255 - i)


def test_flip_bits():
    test_input = bytes(b"ABCDEFGHIJNLMNOPQRSTUVWXYZabcdefghijnlmnopqrstuvwxyz1234567890!@#$%^&*()")
    expected_output = (
        b"\xbe\xbd\xbc\xbb\xba\xb9\xb8\xb7\xb6\xb5\xb1\xb3\xb2\xb1\xb0\xaf\xae\xad"
        b"\xac\xab\xaa\xa9\xa8\xa7\xa6\xa5\x9e\x9d\x9c\x9b\x9a\x99\x98\x97\x96\x95"
        b"\x91\x93\x92\x91\x90\x8f\x8e\x8d\x8c\x8b\x8a\x89\x88\x87\x86\x85\xce\xcd"
        b"\xcc\xcb\xca\xc9\xc8\xc7\xc6\xcf\xde\xbf\xdc\xdb\xda\xa1\xd9\xd5\xd7\xd6"
    )

    assert bit_manipulators.flip_bits(test_input) == expected_output


def test_flip_bits__reversible():
    test_input = bytes(
        b"ABCDEFGHIJNLM\xffNOPQRSTUVWXYZabcde\xf5fghijnlmnopqr\xC3stuvwxyz1\x87234567890!@#$%^&*()"
    )

    test_output = bit_manipulators.flip_bits(test_input)
    test_output = bit_manipulators.flip_bits(test_output)

    assert test_input == test_output

import io

from common.utils.file_utils import (
    append_bytes,
    make_fileobj_copy,
)


def test_make_fileobj_copy():
    TEST_STR = b"Hello World"
    with io.BytesIO(TEST_STR) as src:
        dst = make_fileobj_copy(src)

        # Writing the assertion this way verifies that both src and dest file handles have had
        # their positions reset to 0.
        assert src.read() == TEST_STR
        assert dst.read() == TEST_STR


def test_make_fileobj_copy_seek_src_to_0():
    TEST_STR = b"Hello World"
    with io.BytesIO(TEST_STR) as src:
        src.seek(int(len(TEST_STR) / 2))
        dst = make_fileobj_copy(src)

        # Writing the assertion this way verifies that both src and dest file handles have had
        # their positions reset to 0.
        assert src.read() == TEST_STR
        assert dst.read() == TEST_STR


def test_append_bytes__pos_0():
    bytes_io = io.BytesIO(b"1234 5678")

    append_bytes(bytes_io, b"abcd")

    assert bytes_io.read() == b"1234 5678abcd"


def test_append_bytes__pos_5():
    bytes_io = io.BytesIO(b"1234 5678")
    bytes_io.seek(5, io.SEEK_SET)

    append_bytes(bytes_io, b"abcd")

    assert bytes_io.read() == b"5678abcd"
    bytes_io.seek(0, io.SEEK_SET)
    assert bytes_io.read() == b"1234 5678abcd"

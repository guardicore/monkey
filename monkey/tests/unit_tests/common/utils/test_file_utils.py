import io

from common.utils.file_utils import append_bytes


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

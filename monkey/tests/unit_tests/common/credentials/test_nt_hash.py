import pytest

from common.credentials import NTHash


def test_construct_valid_nt_hash(valid_ntlm_hash):
    # This test will fail if an exception is raised
    NTHash(nt_hash=valid_ntlm_hash)


def test_construct_invalid_nt_hash(invalid_ntlm_hashes):
    for invalid_hash in invalid_ntlm_hashes:
        with pytest.raises(ValueError):
            NTHash(nt_hash=invalid_hash)

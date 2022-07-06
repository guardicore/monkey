import pytest

from common.credentials import InvalidCredentialComponent, LMHash, NTHash

VALID_HASH = "E520AC67419A9A224A3B108F3FA6CB6D"
INVALID_HASHES = (
    0,
    1,
    2.0,
    "invalid",
    "0123456789012345678901234568901",
    "E52GAC67419A9A224A3B108F3FA6CB6D",
)


@pytest.mark.parametrize("ntlm_hash_class", (LMHash, NTHash))
def test_construct_valid_ntlm_hash(ntlm_hash_class):
    # This test will fail if an exception is raised
    ntlm_hash_class(VALID_HASH)


@pytest.mark.parametrize("ntlm_hash_class", (LMHash, NTHash))
def test_construct_invalid_ntlm_hash(ntlm_hash_class):
    for invalid_hash in INVALID_HASHES:
        with pytest.raises(InvalidCredentialComponent):
            ntlm_hash_class(invalid_hash)

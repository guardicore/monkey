from itertools import chain, compress

import pytest

from infection_monkey.utils.brute_force import (
    generate_identity_secret_pairs,
    generate_username_password_or_ntlm_hash_combinations,
)

USERNAMES = ["shaggy", "scooby"]
PASSWORDS = ["1234", "iloveyou", "the_cake_is_a_lie"]
EXPECTED_USERNAME_PASSWORD_PAIRS = {
    (USERNAMES[0], PASSWORDS[0]),
    (USERNAMES[0], PASSWORDS[1]),
    (USERNAMES[0], PASSWORDS[2]),
    (USERNAMES[1], PASSWORDS[0]),
    (USERNAMES[1], PASSWORDS[1]),
    (USERNAMES[1], PASSWORDS[2]),
}

LM_HASHES = ["DEADBEEF", "FACADE"]
EXPECTED_USERNAME_LM_PAIRS = {
    (USERNAMES[0], LM_HASHES[0]),
    (USERNAMES[0], LM_HASHES[1]),
    (USERNAMES[1], LM_HASHES[0]),
    (USERNAMES[1], LM_HASHES[1]),
}

NT_HASHES = ["FADED", "ADDED"]
EXPECTED_USERNAME_NT_PAIRS = {
    (USERNAMES[0], NT_HASHES[0]),
    (USERNAMES[0], NT_HASHES[1]),
    (USERNAMES[1], NT_HASHES[0]),
    (USERNAMES[1], NT_HASHES[1]),
}


def test_generate_username_password_pairs():
    generated_pairs = generate_identity_secret_pairs(USERNAMES, PASSWORDS)
    assert set(generated_pairs) == EXPECTED_USERNAME_PASSWORD_PAIRS


@pytest.mark.parametrize("usernames, passwords", [(USERNAMES, []), ([], PASSWORDS), ([], [])])
def test_generate_username_password_pairs__empty_inputs(usernames, passwords):
    generated_pairs = generate_identity_secret_pairs(usernames, passwords)
    assert len(set(generated_pairs)) == 0


def generate_expected_username_password_hash_combinations(
    passwords: bool, lm_hashes: bool, nt_hashes: bool
):
    possible_combinations = (
        {(p[0], p[1], "", "") for p in EXPECTED_USERNAME_PASSWORD_PAIRS},
        {(p[0], "", p[1], "") for p in EXPECTED_USERNAME_LM_PAIRS},
        {(p[0], "", "", p[1]) for p in EXPECTED_USERNAME_NT_PAIRS},
    )

    return set(
        chain.from_iterable(compress(possible_combinations, (passwords, lm_hashes, nt_hashes)))
    )


def test_generate_username_password_or_ntlm_hash_pairs__empty_usernames():
    generated_pairs = generate_username_password_or_ntlm_hash_combinations(
        [], PASSWORDS, LM_HASHES, NT_HASHES
    )

    assert len(set(generated_pairs)) == 0


@pytest.mark.parametrize(
    "passwords,lm_hashes,nt_hashes",
    [
        (PASSWORDS, LM_HASHES, NT_HASHES),
        ([], LM_HASHES, NT_HASHES),
        (PASSWORDS, [], NT_HASHES),
        (PASSWORDS, LM_HASHES, []),
        (PASSWORDS, [], []),
        ([], LM_HASHES, []),
        ([], [], NT_HASHES),
        ([], [], []),
    ],
)
def test_generate_username_password_or_ntlm_hash_pairs__with_usernames(
    passwords, lm_hashes, nt_hashes
):
    expected_credential_combinations = generate_expected_username_password_hash_combinations(
        bool(passwords), bool(lm_hashes), bool(nt_hashes)
    )
    generated_pairs = generate_username_password_or_ntlm_hash_combinations(
        USERNAMES, passwords, lm_hashes, nt_hashes
    )

    assert set(generated_pairs) == expected_credential_combinations

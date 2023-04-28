import pytest

from infection_monkey.utils.brute_force import generate_identity_secret_pairs

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


def test_generate_username_password_pairs():
    generated_pairs = generate_identity_secret_pairs(USERNAMES, PASSWORDS)
    assert set(generated_pairs) == EXPECTED_USERNAME_PASSWORD_PAIRS


@pytest.mark.parametrize("usernames, passwords", [(USERNAMES, []), ([], PASSWORDS), ([], [])])
def test_generate_username_password_pairs__empty_inputs(usernames, passwords):
    generated_pairs = generate_identity_secret_pairs(usernames, passwords)
    assert len(set(generated_pairs)) == 0

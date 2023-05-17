import pytest

from common.credentials import EmailAddress


@pytest.mark.parametrize("email_address", ["qwerty@gmail.com", "qwe$rty@yahoo.in", "a-b_c@x.y.com"])
def test_construct_valid_email_address(email_address):
    # This test will fail if an exception is raised
    EmailAddress(email_address=email_address)


@pytest.mark.parametrize(
    "email_address",
    [
        "???",
        "validate-me!!!",
        "two-is-too-many@@gmail.com",
        "too far@gmail.com",
        "do-not-pass-this-is-a-threat",
        "too_many_dots@here..com",
        "...@xyz.in",
        "xyz@.mail.com",
        "qwerty@gma$il.com",
    ],
)
def test_construct_invalid_email_address(email_address):
    with pytest.raises(ValueError):
        EmailAddress(email_address=email_address)

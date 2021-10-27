from infection_monkey.utils.random_password_generator import get_random_password


def test_get_random_password__length():
    password_length = len(get_random_password())
    # 32 is the recommended secure byte length for secrets
    assert password_length == 32


def test_get_random_password__custom_length():
    password_length = len(get_random_password(14))
    assert password_length == 14


def test_get_random_password__randomness():
    random_password1 = get_random_password()
    random_password2 = get_random_password()
    assert random_password1 != random_password2

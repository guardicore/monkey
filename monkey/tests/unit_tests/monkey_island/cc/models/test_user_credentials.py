from monkey_island.cc.models import UserCredentials

TEST_USER = "Test"
TEST_HASH = "abc1231234"


def test_bool_true():
    assert UserCredentials(TEST_USER, TEST_HASH)


def test_bool_false_empty_password_hash():
    assert not UserCredentials(TEST_USER, "")


def test_bool_false_empty_user():
    assert not UserCredentials("", TEST_HASH)


def test_bool_false_empty_user_and_password_hash():
    assert not UserCredentials("", "")


def test_to_dict_empty_creds():
    user_creds = UserCredentials("", "")
    assert user_creds.to_dict() == {}


def test_to_dict_full_creds():
    user_creds = UserCredentials(TEST_USER, TEST_HASH)
    assert user_creds.to_dict() == {"user": TEST_USER, "password_hash": TEST_HASH}


def test_member_values(monkeypatch):
    creds = UserCredentials(TEST_USER, TEST_HASH)
    assert creds.username == TEST_USER
    assert creds.password_hash == TEST_HASH

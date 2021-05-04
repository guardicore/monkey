import bcrypt

from monkey_island.cc.environment.user_creds import UserCreds

TEST_SALT = b"$2b$12$JA7GdT1iyfIsquF2cTZv2."


def test_to_dict_empty_creds():
    user_creds = UserCreds()
    assert user_creds.to_dict() == {}


def test_to_dict_full_creds():
    user_creds = UserCreds(username="Test", password_hash="abc1231234")
    assert user_creds.to_dict() == {"user": "Test", "password_hash": "abc1231234"}


def test_to_auth_user_full_credentials():
    user_creds = UserCreds(username="Test", password_hash="abc1231234")
    auth_user = user_creds.to_auth_user()
    assert auth_user.id == 1
    assert auth_user.username == "Test"
    assert auth_user.secret == "abc1231234"


def test_to_auth_user_username_only():
    user_creds = UserCreds(username="Test")
    auth_user = user_creds.to_auth_user()
    assert auth_user.id == 1
    assert auth_user.username == "Test"
    assert auth_user.secret == ""


def test_get_from_cleartext(monkeypatch):
    monkeypatch.setattr(bcrypt, "gensalt", lambda: TEST_SALT)

    creds = UserCreds.from_cleartext("Test", "Test_Password")
    assert creds.password_hash == "$2b$12$JA7GdT1iyfIsquF2cTZv2.NdGFuYbX1WGfQAOyHlpEsgDTNGZ0TXG"

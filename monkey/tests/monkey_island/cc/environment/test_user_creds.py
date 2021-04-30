from monkey_island.cc.environment.user_creds import UserCreds


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

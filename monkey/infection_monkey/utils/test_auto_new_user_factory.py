import pytest

import infection_monkey.utils.auto_new_user_factory as new_user_factory


class NewUserStub:
    def __init__(self, username, password):
        pass


class NewWindowsUserStub(NewUserStub):
    pass


class NewLinuxUserStub(NewUserStub):
    pass


@pytest.fixture
def patch_new_user_classes(monkeypatch):
    monkeypatch.setattr(new_user_factory, "AutoNewWindowsUser", NewWindowsUserStub)
    monkeypatch.setattr(new_user_factory, "AutoNewLinuxUser", NewLinuxUserStub)


def test_create_auto_new_user_windows_user(patch_new_user_classes):
    new_user = new_user_factory.create_auto_new_user("user", "password", True)

    assert isinstance(new_user, NewWindowsUserStub)


def test_create_auto_new_user_linux_user(patch_new_user_classes):
    new_user = new_user_factory.create_auto_new_user("user", "password", False)

    assert isinstance(new_user, NewLinuxUserStub)

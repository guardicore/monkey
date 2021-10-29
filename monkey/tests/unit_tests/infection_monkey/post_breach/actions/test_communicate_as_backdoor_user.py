from infection_monkey.post_breach.actions.communicate_as_backdoor_user import (
    USERNAME_PREFIX,
    CommunicateAsBackdoorUser,
)

URL = "this-is-where-i-wanna-go"


def test_get_random_new_user_name():
    username = CommunicateAsBackdoorUser.get_random_new_user_name()
    assert len(username) == len(USERNAME_PREFIX) + 5
    assert username.islower()
    assert username.startswith(USERNAME_PREFIX)


def test_get_commandline_for_http_request_windows():
    cmd_line = CommunicateAsBackdoorUser.get_commandline_for_http_request(URL, is_windows=True)
    assert "powershell.exe" in cmd_line
    assert URL in cmd_line


def test_get_commandline_for_http_request_linux_curl(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.post_breach.actions.communicate_as_backdoor_user.shutil.which",
        lambda _: "not None",
    )
    cmd_line = CommunicateAsBackdoorUser.get_commandline_for_http_request(URL, is_windows=False)
    assert "curl" in cmd_line
    assert URL in cmd_line


def test_get_commandline_for_http_request_linux_wget(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.post_breach.actions.communicate_as_backdoor_user.shutil.which",
        lambda _: None,
    )
    cmd_line = CommunicateAsBackdoorUser.get_commandline_for_http_request(URL, is_windows=False)
    assert "wget" in cmd_line
    assert URL in cmd_line

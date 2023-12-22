from pathlib import Path
from threading import Event

import pytest
from agent_plugins.credentials_collectors.chrome.src.browser_credentials_database_path import (
    BrowserCredentialsDatabasePath,
)
from monkeytypes import Credentials, EmailAddress, Password, Username

pwd = pytest.importorskip("pwd")
# we need to check if `pwd` can be imported before importing `LinuxCredentialsDatabaseProcessor`
from agent_plugins.credentials_collectors.chrome.src.linux_credentials_database_processor import (  # noqa: E402, E501
    LinuxCredentialsDatabaseProcessor,
)

LOGINS_A = [
    ("user1", b"v1037\xbc\xae\x8c\x1e\x19&+\xf0S\x14\x02E\xf2\xcf"),
    ("user2", b"v10\xa0\x0b\xca\xb5\xfe\x96\x05m\x91\x97lY-\xcf\xcaz"),
]
LOGINS_B = [("user3@email.com", b"v10\x1c)\xa9\x10[\x87\xdf(F\xbdMx\x91\x84\xdf\xfc")]
LOGINS_C = [("user4", b"v11pass")]
CREDENTIALS_A = [
    Credentials(identity=Username(username="user1"), secret=Password(password="user1pass")),
    Credentials(identity=Username(username="user2"), secret=Password(password="user2pass")),
]
CREDENTIALS_B = [
    Credentials(
        identity=EmailAddress(email_address="user3@email.com"),
        secret=Password(password="user3pass"),
    )
]
CREDENTIALS_C = [
    Credentials(identity=Username(username="user4"), secret=Password(password="user4pass"))
]
PROFILE_A_PATH = BrowserCredentialsDatabasePath(Path("profile_a"), None)
PROFILE_B_PATH = BrowserCredentialsDatabasePath(Path("profile_b"), None)
PROFILE_C_PATH = BrowserCredentialsDatabasePath(Path("profile_c"), None)


@pytest.fixture
def mock_database_reader():
    def get_credentials(database_path):
        profile = str(database_path)
        if profile == "profile_a":
            yield from LOGINS_A
        elif profile == "profile_b":
            yield from LOGINS_B
        elif profile == "profile_c":
            yield from LOGINS_C

    return get_credentials


@pytest.fixture
def credentials_database_processor(mock_database_reader) -> LinuxCredentialsDatabaseProcessor:
    return LinuxCredentialsDatabaseProcessor(mock_database_reader)


def test_is_interruptible(credentials_database_processor):
    event = Event()
    event.set()
    credentials = credentials_database_processor(interrupt=event, database_paths=[PROFILE_A_PATH])

    assert len(credentials) == 0


def test_parses_usernames(credentials_database_processor):
    credentials = credentials_database_processor(interrupt=Event(), database_paths=[PROFILE_A_PATH])

    assert len(credentials) == 2
    for credential in CREDENTIALS_A:
        assert credential in credentials


def test_parses_email_addresses(credentials_database_processor):
    credentials = credentials_database_processor(interrupt=Event(), database_paths=[PROFILE_B_PATH])

    assert len(credentials) == 1
    assert CREDENTIALS_B[0] in credentials


# If we ever add support for password wallets, we'll need to update this.
def test_fails_to_decrypt_wallet_encrypted_passwords(credentials_database_processor):
    credentials = credentials_database_processor(interrupt=Event(), database_paths=[PROFILE_C_PATH])

    assert len(credentials) == 1
    assert credentials[0].identity == CREDENTIALS_C[0].identity
    assert credentials[0].secret is None

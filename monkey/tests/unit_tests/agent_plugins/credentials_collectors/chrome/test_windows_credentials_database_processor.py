import sys
from pathlib import Path
from threading import Event
from unittest.mock import MagicMock

import pytest
from agent_plugins.credentials_collectors.chrome.src.browser_credentials_database_path import (
    BrowserCredentialsDatabasePath,
)
from tests.utils import get_reference_to_exception_raising_function

from common.credentials import Credentials, EmailAddress, Password, Username

LOGINS_A = [("user1", b"password1"), ("user2", b"password2")]
LOGINS_B = [("user3@email.com", b"password3")]
LOGINS_C = [
    ("user4", b"v10blahblahblah~\xf5\xb4)+=\xceH&\x18M\xd9\xf2\x94#\x12\xa7\xbf\xe2\x96\xc5RH\xbco")
]
CREDENTIALS_A = [
    Credentials(identity=Username(username="user1"), secret=Password(password="password1")),
    Credentials(identity=Username(username="user2"), secret=Password(password="password2")),
]
CREDENTIALS_B = [
    Credentials(
        identity=EmailAddress(email_address="user3@email.com"),
        secret=Password(password="password3"),
    )
]
CREDENTIALS_C = [
    Credentials(
        identity=Username(username="user4"),
        secret=Password(password="password4"),
    )
]
PROFILE_A = BrowserCredentialsDatabasePath(Path("profile_a"), b"master_key")
PROFILE_B = BrowserCredentialsDatabasePath(Path("profile_b"), b"master_key")
PROFILE_C = BrowserCredentialsDatabasePath(
    Path("profile_c"), b"\xfdb\x1f\xe5\xa2\xb4\x02S\x9d\xfa\x14|\xa9''x"
)


@pytest.fixture(scope="module", autouse=True)
def patch_windows_decryption():
    def mock_win32crypt_unprotect_data(master_key):
        return master_key

    windows_decryption = MagicMock()
    windows_decryption.win32crypt_unprotect_data = mock_win32crypt_unprotect_data
    sys.modules[
        "agent_plugins.credentials_collectors.chrome.src.windows_decryption"
    ] = windows_decryption


@pytest.fixture
def mock_database_reader():
    def mock_get_logins_from_database(database_path):
        profile = str(database_path)
        if profile == "profile_a":
            yield from LOGINS_A
        elif profile == "profile_b":
            yield from LOGINS_B
        elif profile == "profile_c":
            yield from LOGINS_C

    return mock_get_logins_from_database


@pytest.fixture
def credentials_database_processor(mock_database_reader):
    from agent_plugins.credentials_collectors.chrome.src.windows_credentials_database_processor import (  # noqa: E501
        WindowsCredentialsDatabaseProcessor,
    )

    return WindowsCredentialsDatabaseProcessor(mock_database_reader)


def test_extracts_credentials(credentials_database_processor):
    credentials = credentials_database_processor(Event(), [PROFILE_A])

    assert len(credentials) == 2
    for item in CREDENTIALS_A:
        assert item in credentials


def test_extracts_email_addresses(credentials_database_processor):
    credentials = credentials_database_processor(Event(), [PROFILE_B])

    assert len(credentials) == 1
    assert CREDENTIALS_B[0] in credentials


def test_is_interruptible(credentials_database_processor):
    interrupt = Event()
    interrupt.set()
    credentials = credentials_database_processor(interrupt, [PROFILE_A])
    assert len(credentials) == 0


def test_decrypts_password_with_master_key(credentials_database_processor):
    credentials = credentials_database_processor(Event(), [PROFILE_C])

    assert len(credentials) == 1
    assert CREDENTIALS_C[0] in credentials


def test_username_credential_saved_if_decrypt_password_fails(credentials_database_processor):
    credentials_database_processor._decrypt_password = lambda *_: None

    credentials = credentials_database_processor(Event(), [PROFILE_C])
    expected_credentials = [Credentials(identity=CREDENTIALS_C[0].identity)]

    assert len(credentials) == 1
    assert expected_credentials == credentials


def test_username_credential_saved_if_win32crypt_unprotect_data_fails(
    monkeypatch, credentials_database_processor
):
    monkeypatch.setattr(
        "agent_plugins.credentials_collectors.chrome.src."
        "windows_credentials_database_processor.win32crypt_unprotect_data",
        get_reference_to_exception_raising_function(Exception),
    )

    credentials = credentials_database_processor(Event(), [PROFILE_B])
    expected_credentials = [Credentials(identity=CREDENTIALS_B[0].identity)]

    assert len(credentials) == 1
    assert expected_credentials == credentials


def test_username_credential_saved_if_decrypted_password_is_empty(
    monkeypatch, credentials_database_processor
):
    mocked_decrypt_v80 = MagicMock(return_value="")
    monkeypatch.setattr(
        "agent_plugins.credentials_collectors.chrome.src."
        "windows_credentials_database_processor.decrypt_v80",
        mocked_decrypt_v80,
    )

    credentials = credentials_database_processor(Event(), [PROFILE_C])
    expected_credentials = [Credentials(identity=CREDENTIALS_C[0].identity)]

    assert len(credentials) == 1
    assert expected_credentials == credentials


def test_username_credential_saved_if_error_decrypting_password(
    monkeypatch, credentials_database_processor
):
    mocked_decrypt_v80 = MagicMock(side_effect=ValueError)
    monkeypatch.setattr(
        "agent_plugins.credentials_collectors.chrome.src."
        "windows_credentials_database_processor.decrypt_v80",
        mocked_decrypt_v80,
    )

    credentials = credentials_database_processor(Event(), [PROFILE_C])
    expected_credentials = [Credentials(identity=CREDENTIALS_C[0].identity)]

    assert len(credentials) == 1
    assert expected_credentials == credentials


def test_fails_to_extract_credentials_if_master_key_is_none(credentials_database_processor):
    profile = BrowserCredentialsDatabasePath(PROFILE_C.database_file_path, None)
    credentials = credentials_database_processor(Event(), [profile])

    assert len(credentials) == 1
    for item in credentials:
        assert item.secret is None

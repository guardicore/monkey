import mongoengine
import pytest

from common.credentials import Credentials
from monkey_island.cc.repository import MongoCredentialsRepository

USER1 = "test_user_1"
USER2 = "test_user_2"
USER3 = "test_user_3"
PASSWORD = "12435"
PASSWORD2 = "password"
PASSWORD3 = "lozinka"
LM_HASH = "AEBD4DE384C7EC43AAD3B435B51404EE"
NT_HASH = "7A21990FCD3D759941E45C490F143D5F"
PUBLIC_KEY = "MY_PUBLIC_KEY"
PRIVATE_KEY = "MY_PRIVATE_KEY"

CREDENTIALS_DICT_1 = {
    "identities": [
        {"credential_type": "USERNAME", "username": USER1},
        {"credential_type": "USERNAME", "username": USER2},
    ],
    "secrets": [
        {"credential_type": "PASSWORD", "password": PASSWORD},
        {"credential_type": "LM_HASH", "lm_hash": LM_HASH},
        {"credential_type": "NT_HASH", "nt_hash": NT_HASH},
        {
            "credential_type": "SSH_KEYPAIR",
            "public_key": PUBLIC_KEY,
            "private_key": PRIVATE_KEY,
        },
    ],
}

CREDENTIALS_DICT_2 = {
    "identities": [
        {"credential_type": "USERNAME", "username": USER3},
    ],
    "secrets": [
        {"credential_type": "PASSWORD", "password": PASSWORD2},
        {"credential_type": "PASSWORD", "password": PASSWORD3},
    ],
}

CONFIGURED_CREDENTIALS = [Credentials.from_mapping(CREDENTIALS_DICT_1)]

STOLEN_CREDENTIALS = [Credentials.from_mapping(CREDENTIALS_DICT_2)]

CREDENTIALS_LIST = [
    Credentials.from_mapping(CREDENTIALS_DICT_1),
    Credentials.from_mapping(CREDENTIALS_DICT_2),
]


@pytest.fixture
def fake_mongo_repository(monkeypatch):
    mongo = mongoengine.connection.get_connection()
    return MongoCredentialsRepository(mongo)


def test_mongo_repository_get_configured(fake_mongo_repository):

    actual_configured_credentials = fake_mongo_repository.get_configured_credentials()

    assert actual_configured_credentials == []


def test_mongo_repository_get_stolen(fake_mongo_repository):

    actual_stolen_credentials = fake_mongo_repository.get_stolen_credentials()

    assert actual_stolen_credentials == []


def test_mongo_repository_get_all(fake_mongo_repository):

    actual_credentials = fake_mongo_repository.get_all_credentials()

    assert actual_credentials == []


def test_mongo_repository_configured(fake_mongo_repository):

    fake_mongo_repository.save_configured_credentials(CREDENTIALS_LIST)

    actual_configured_credentials = fake_mongo_repository.get_configured_credentials()

    assert actual_configured_credentials == CREDENTIALS_LIST

    fake_mongo_repository.remove_configured_credentials()

    actual_configured_credentials = fake_mongo_repository.get_configured_credentials()

    assert actual_configured_credentials == []


def test_mongo_repository_stolen(fake_mongo_repository):

    fake_mongo_repository.save_configured_credentials(CONFIGURED_CREDENTIALS)
    fake_mongo_repository.save_stolen_credentials(STOLEN_CREDENTIALS)

    actual_stolen_credentials = fake_mongo_repository.get_stolen_credentials()

    assert actual_stolen_credentials == STOLEN_CREDENTIALS

    fake_mongo_repository.remove_stolen_credentials()

    actual_stolen_credentials = fake_mongo_repository.get_stolen_credentials()

    assert actual_stolen_credentials == []

    # Must remove configured also for the next tests
    fake_mongo_repository.remove_configured_credentials()


def test_mongo_repository_all(fake_mongo_repository):

    fake_mongo_repository.save_configured_credentials(CONFIGURED_CREDENTIALS)
    fake_mongo_repository.save_stolen_credentials(STOLEN_CREDENTIALS)

    actual_credentials = fake_mongo_repository.get_all_credentials()

    assert actual_credentials == CREDENTIALS_LIST

    fake_mongo_repository.remove_all_credentials()

    actual_credentials = fake_mongo_repository.get_all_credentials()
    actual_stolen_credentials = fake_mongo_repository.get_stolen_credentials()
    actual_configured_credentials = fake_mongo_repository.get_configured_credentials()

    assert actual_credentials == []
    assert actual_stolen_credentials == []
    assert actual_configured_credentials == []

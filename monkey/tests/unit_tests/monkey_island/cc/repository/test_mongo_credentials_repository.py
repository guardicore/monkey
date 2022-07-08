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


@pytest.fixture
def fake_mongo(monkeypatch):
    mongo = mongoengine.connection.get_connection()
    monkeypatch.setattr("monkey_island.cc.repository.mongo_credentials_repository.mongo", mongo)


def test_mongo_repository_get_configured(fake_mongo):

    actual_configured_credentials = MongoCredentialsRepository().get_configured_credentials()

    assert actual_configured_credentials == []


def test_mongo_repository_get_stolen(fake_mongo):

    actual_stolen_credentials = MongoCredentialsRepository().get_stolen_credentials()

    assert actual_stolen_credentials == []


def test_mongo_repository_get_all(fake_mongo):

    actual_credentials = MongoCredentialsRepository().get_all_credentials()

    assert actual_credentials == []


def test_mongo_repository_configured(fake_mongo):

    credentials = [
        Credentials.from_mapping(CREDENTIALS_DICT_1),
        Credentials.from_mapping(CREDENTIALS_DICT_2),
    ]

    mongo_repository = MongoCredentialsRepository()
    mongo_repository.save_configured_credentials(credentials)

    actual_configured_credentials = mongo_repository.get_configured_credentials()

    assert actual_configured_credentials == credentials

    mongo_repository.remove_configured_credentials()

    actual_configured_credentials = mongo_repository.get_configured_credentials()

    assert actual_configured_credentials == []


def test_mongo_repository_stolen(fake_mongo):

    stolen_credentials = [Credentials.from_mapping(CREDENTIALS_DICT_1)]

    configured_credentials = [Credentials.from_mapping(CREDENTIALS_DICT_2)]

    mongo_repository = MongoCredentialsRepository()
    mongo_repository.save_configured_credentials(configured_credentials)
    mongo_repository.save_stolen_credentials(stolen_credentials)

    actual_stolen_credentials = mongo_repository.get_stolen_credentials()

    assert actual_stolen_credentials == stolen_credentials

    mongo_repository.remove_stolen_credentials()

    actual_stolen_credentials = mongo_repository.get_stolen_credentials()

    assert actual_stolen_credentials == []

    # Must remove configured also for the next tests
    mongo_repository.remove_configured_credentials()


def test_mongo_repository_all(fake_mongo):

    configured_credentials = [Credentials.from_mapping(CREDENTIALS_DICT_1)]
    stolen_credentials = [Credentials.from_mapping(CREDENTIALS_DICT_2)]
    all_credentials = [
        Credentials.from_mapping(CREDENTIALS_DICT_1),
        Credentials.from_mapping(CREDENTIALS_DICT_2),
    ]

    mongo_repository = MongoCredentialsRepository()
    mongo_repository.save_configured_credentials(configured_credentials)
    mongo_repository.save_stolen_credentials(stolen_credentials)

    actual_credentials = mongo_repository.get_all_credentials()

    assert actual_credentials == all_credentials

    mongo_repository.remove_all_credentials()

    actual_credentials = mongo_repository.get_all_credentials()
    actual_stolen_credentials = mongo_repository.get_stolen_credentials()
    actual_configured_credentials = mongo_repository.get_configured_credentials()

    assert actual_credentials == []
    assert actual_stolen_credentials == []
    assert actual_configured_credentials == []

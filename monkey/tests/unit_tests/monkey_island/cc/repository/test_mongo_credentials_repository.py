from unittest.mock import MagicMock

import mongomock
import pytest
from tests.data_for_tests.propagation_credentials import PROPAGATION_CREDENTIALS

from common.credentials import Credentials, LMHash, NTHash, Password, SSHKeypair, Username
from monkey_island.cc.repository import MongoCredentialsRepository
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

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

IDENTITIES_1 = (Username(USER1), Username(USER2))
SECRETS_1 = (
    Password(PASSWORD),
    LMHash(LM_HASH),
    NTHash(NT_HASH),
    SSHKeypair(PRIVATE_KEY, PUBLIC_KEY),
)
CREDENTIALS_OBJECT_1 = Credentials(IDENTITIES_1, SECRETS_1)

IDENTITIES_2 = (Username(USER3),)
SECRETS_2 = (Password(PASSWORD2), Password(PASSWORD3))
CREDENTIALS_OBJECT_2 = Credentials(IDENTITIES_2, SECRETS_2)


CONFIGURED_CREDENTIALS = PROPAGATION_CREDENTIALS[0:3]

STOLEN_CREDENTIALS = PROPAGATION_CREDENTIALS[3:6]

CREDENTIALS_LIST = [CREDENTIALS_OBJECT_1, CREDENTIALS_OBJECT_2]


def reverse(data: bytes) -> bytes:
    return bytes(reversed(data))


@pytest.fixture
def repository_encryptor():
    repository_encryptor = MagicMock(spec=ILockableEncryptor)
    repository_encryptor.encrypt = MagicMock(side_effect=reverse)
    repository_encryptor.decrypt = MagicMock(side_effect=reverse)

    return repository_encryptor


@pytest.fixture
def mongo_client():
    return mongomock.MongoClient()


@pytest.fixture
def mongo_repository(mongo_client, repository_encryptor):
    return MongoCredentialsRepository(mongo_client, repository_encryptor)


def test_mongo_repository_get_configured(mongo_repository):
    actual_configured_credentials = mongo_repository.get_configured_credentials()

    assert actual_configured_credentials == []


def test_mongo_repository_get_stolen(mongo_repository):
    actual_stolen_credentials = mongo_repository.get_stolen_credentials()

    assert actual_stolen_credentials == []


def test_mongo_repository_get_all(mongo_repository):
    actual_credentials = mongo_repository.get_all_credentials()

    assert actual_credentials == []


def test_mongo_repository_configured(mongo_repository):
    mongo_repository.save_configured_credentials(PROPAGATION_CREDENTIALS)
    actual_configured_credentials = mongo_repository.get_configured_credentials()
    assert actual_configured_credentials == PROPAGATION_CREDENTIALS

    mongo_repository.remove_configured_credentials()
    actual_configured_credentials = mongo_repository.get_configured_credentials()
    assert actual_configured_credentials == []


def test_mongo_repository_stolen(mongo_repository):
    mongo_repository.save_stolen_credentials(STOLEN_CREDENTIALS)
    actual_stolen_credentials = mongo_repository.get_stolen_credentials()
    assert actual_stolen_credentials == STOLEN_CREDENTIALS

    mongo_repository.remove_stolen_credentials()
    actual_stolen_credentials = mongo_repository.get_stolen_credentials()
    assert actual_stolen_credentials == []


def test_mongo_repository_all(mongo_repository):
    mongo_repository.save_configured_credentials(CONFIGURED_CREDENTIALS)
    mongo_repository.save_stolen_credentials(STOLEN_CREDENTIALS)
    actual_credentials = mongo_repository.get_all_credentials()
    assert actual_credentials == PROPAGATION_CREDENTIALS

    mongo_repository.remove_all_credentials()

    assert mongo_repository.get_all_credentials() == []
    assert mongo_repository.get_stolen_credentials() == []
    assert mongo_repository.get_configured_credentials() == []


# NOTE: The following tests are complicated, but they work. Rather than spend the effort to improve
#       them now, we can revisit them when we resolve #2072. Resolving #2072 will make it easier to
#       simplify these tests.
@pytest.mark.parametrize("credentials", PROPAGATION_CREDENTIALS)
def test_configured_secrets_encrypted(mongo_repository, mongo_client, credentials):
    mongo_repository.save_configured_credentials([credentials])
    check_if_stored_credentials_encrypted(mongo_client, credentials)


@pytest.mark.parametrize("credentials", PROPAGATION_CREDENTIALS)
def test_stolen_secrets_encrypted(mongo_repository, mongo_client, credentials):
    mongo_repository.save_stolen_credentials([credentials])
    check_if_stored_credentials_encrypted(mongo_client, credentials)


def check_if_stored_credentials_encrypted(mongo_client, original_credentials):
    raw_credentials = get_all_credentials_in_mongo(mongo_client)
    original_credentials_mapping = Credentials.to_mapping(original_credentials)
    for rc in raw_credentials:
        for identity_or_secret, credentials_component in rc.items():
            for key, value in credentials_component.items():
                assert original_credentials_mapping[identity_or_secret][key] != value


def get_all_credentials_in_mongo(mongo_client):
    encrypted_credentials = []

    # Loop through all databases and collections and search for credentials. We don't want the tests
    # to assume anything about the internal workings of the repository.
    for db in mongo_client.list_database_names():
        for collection in mongo_client[db].list_collection_names():
            mongo_credentials = mongo_client[db][collection].find({})
            for mc in mongo_credentials:
                del mc["_id"]
                encrypted_credentials.append(mc)

    return encrypted_credentials

import mongomock
import pytest

from common.credentials import Credentials, LMHash, NTHash, Password, SSHKeypair, Username
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


CONFIGURED_CREDENTIALS = [CREDENTIALS_OBJECT_1]

STOLEN_CREDENTIALS = [CREDENTIALS_OBJECT_2]

CREDENTIALS_LIST = [CREDENTIALS_OBJECT_1, CREDENTIALS_OBJECT_2]


@pytest.fixture
def mongo_repository():
    mongo = mongomock.MongoClient()

    return MongoCredentialsRepository(mongo)


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

    mongo_repository.save_configured_credentials(CREDENTIALS_LIST)

    actual_configured_credentials = mongo_repository.get_configured_credentials()

    assert actual_configured_credentials == CREDENTIALS_LIST

    mongo_repository.remove_configured_credentials()

    actual_configured_credentials = mongo_repository.get_configured_credentials()

    assert actual_configured_credentials == []


def test_mongo_repository_stolen(mongo_repository):

    mongo_repository.save_configured_credentials(CONFIGURED_CREDENTIALS)
    mongo_repository.save_stolen_credentials(STOLEN_CREDENTIALS)

    actual_stolen_credentials = mongo_repository.get_stolen_credentials()

    assert actual_stolen_credentials == STOLEN_CREDENTIALS

    mongo_repository.remove_stolen_credentials()

    actual_stolen_credentials = mongo_repository.get_stolen_credentials()

    assert actual_stolen_credentials == []

    # Must remove configured also for the next tests
    mongo_repository.remove_configured_credentials()


def test_mongo_repository_all(mongo_repository):

    mongo_repository.save_configured_credentials(CONFIGURED_CREDENTIALS)
    mongo_repository.save_stolen_credentials(STOLEN_CREDENTIALS)

    actual_credentials = mongo_repository.get_all_credentials()

    assert actual_credentials == CREDENTIALS_LIST

    mongo_repository.remove_all_credentials()

    actual_credentials = mongo_repository.get_all_credentials()
    actual_stolen_credentials = mongo_repository.get_stolen_credentials()
    actual_configured_credentials = mongo_repository.get_configured_credentials()

    assert actual_credentials == []
    assert actual_stolen_credentials == []
    assert actual_configured_credentials == []

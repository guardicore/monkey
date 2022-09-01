from typing import Any, Iterable, Mapping, Sequence
from unittest.mock import MagicMock

import mongomock
import pytest
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from tests.data_for_tests.propagation_credentials import CREDENTIALS

from common.credentials import Credentials
from monkey_island.cc.repository import MongoCredentialsRepository
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

CONFIGURED_CREDENTIALS = CREDENTIALS[0:3]
STOLEN_CREDENTIALS = CREDENTIALS[3:]


def reverse(data: bytes) -> bytes:
    return bytes(reversed(data))


@pytest.fixture
def repository_encryptor():
    # NOTE: Tests will fail if any inputs to this mock encryptor are palindromes.
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
    mongo_repository.save_configured_credentials(CREDENTIALS)
    actual_configured_credentials = mongo_repository.get_configured_credentials()
    assert actual_configured_credentials == CREDENTIALS

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
    assert actual_credentials == CREDENTIALS

    mongo_repository.remove_all_credentials()

    assert mongo_repository.get_all_credentials() == []
    assert mongo_repository.get_stolen_credentials() == []
    assert mongo_repository.get_configured_credentials() == []


@pytest.mark.parametrize("credentials", CREDENTIALS)
def test_configured_secrets_encrypted(
    mongo_repository: MongoCredentialsRepository,
    mongo_client: MongoClient,
    credentials: Sequence[Credentials],
):
    mongo_repository.save_configured_credentials([credentials])
    check_if_stored_credentials_encrypted(mongo_client, credentials)


@pytest.mark.parametrize("credentials", CREDENTIALS)
def test_stolen_secrets_encrypted(mongo_repository, mongo_client, credentials: Credentials):
    mongo_repository.save_stolen_credentials([credentials])
    check_if_stored_credentials_encrypted(mongo_client, credentials)


def check_if_stored_credentials_encrypted(mongo_client: MongoClient, original_credentials):
    original_credentials_mapping = original_credentials.dict()
    raw_credentials = get_all_credentials_in_mongo(mongo_client)

    for rc in raw_credentials:
        for identity_or_secret, credentials_component in rc.items():
            if original_credentials_mapping[identity_or_secret] is None:
                assert credentials_component is None
            else:
                for key, value in credentials_component.items():
                    assert original_credentials_mapping[identity_or_secret][key] != value.decode()


def get_all_credentials_in_mongo(
    mongo_client: MongoClient,
) -> Iterable[Mapping[str, Mapping[str, Any]]]:
    encrypted_credentials = []

    # Loop through all databases and collections and search for credentials. We don't want the tests
    # to assume anything about the internal workings of the repository.
    for collection in get_all_collections_in_mongo(mongo_client):
        mongo_credentials = collection.find({})
        for mc in mongo_credentials:
            del mc["_id"]
            encrypted_credentials.append(mc)

    return encrypted_credentials


def get_all_collections_in_mongo(mongo_client: MongoClient) -> Iterable[Collection]:
    collections = [
        collection
        for db in get_all_databases_in_mongo(mongo_client)
        for collection in get_all_collections_in_database(db)
    ]

    assert len(collections) > 0
    return collections


def get_all_databases_in_mongo(mongo_client) -> Iterable[Database]:
    return (mongo_client[db_name] for db_name in mongo_client.list_database_names())


def get_all_collections_in_database(db: Database) -> Iterable[Collection]:
    return (db[collection_name] for collection_name in db.list_collection_names())

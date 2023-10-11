from typing import Any, Iterable, Mapping
from unittest.mock import MagicMock

import mongomock
import pytest
from monkeytypes import Credentials
from pymongo import MongoClient
from tests.data_for_tests.propagation_credentials import CREDENTIALS
from tests.unit_tests.monkey_island.cc.repositories.mongo import get_all_collections_in_mongo

from monkey_island.cc.repositories import (
    ICredentialsRepository,
    MongoCredentialsRepository,
    RemovalError,
    RetrievalError,
    StorageError,
)
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

CONFIGURED_CREDENTIALS = CREDENTIALS[0:3]
STOLEN_CREDENTIALS = CREDENTIALS[3:]


@pytest.fixture
def mongo_client():
    return mongomock.MongoClient()


@pytest.fixture
def mongo_repository(mongo_client, repository_encryptor):
    return MongoCredentialsRepository(mongo_client, repository_encryptor)


@pytest.fixture
def error_raising_mock_mongo_client() -> mongomock.MongoClient:
    mongo_client = MagicMock(spec=mongomock.MongoClient)
    mongo_client.monkey_island = MagicMock(spec=mongomock.Database)
    mongo_client.monkey_island.stolen_credentials = MagicMock(spec=mongomock.Collection)
    mongo_client.monkey_island.configured_credentials = MagicMock(spec=mongomock.Collection)

    mongo_client.monkey_island.configured_credentials.find = MagicMock(
        side_effect=Exception("some exception")
    )
    mongo_client.monkey_island.stolen_credentials.find = MagicMock(
        side_effect=Exception("some exception")
    )
    mongo_client.monkey_island.stolen_credentials.insert_one = MagicMock(
        side_effect=Exception("some exception")
    )
    mongo_client.monkey_island.stolen_credentials.drop = MagicMock(
        side_effect=Exception("some exception")
    )

    return mongo_client


@pytest.fixture
def error_raising_credentials_repository(
    error_raising_mock_mongo_client: mongomock.MongoClient, repository_encryptor: ILockableEncryptor
) -> ICredentialsRepository:
    return MongoCredentialsRepository(error_raising_mock_mongo_client, repository_encryptor)


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


def test_mongo_repository_get__retrieval_error(error_raising_credentials_repository):
    with pytest.raises(RetrievalError):
        error_raising_credentials_repository.get_all_credentials()


def test_mongo_repository_save__storage_error(error_raising_credentials_repository):
    with pytest.raises(StorageError):
        error_raising_credentials_repository.save_stolen_credentials(STOLEN_CREDENTIALS)


def test_mongo_repository_remove_credentials__removal_error(error_raising_credentials_repository):
    with pytest.raises(RemovalError):
        error_raising_credentials_repository.remove_stolen_credentials()


def test_mongo_repository_reset__removal_error(error_raising_credentials_repository):
    with pytest.raises(RemovalError):
        error_raising_credentials_repository.reset()


@pytest.mark.parametrize("credentials", CREDENTIALS)
def test_configured_secrets_encrypted(
    mongo_repository: MongoCredentialsRepository,
    mongo_client: MongoClient,
    credentials: Credentials,
):
    mongo_repository.save_configured_credentials([credentials])
    check_if_stored_credentials_encrypted(mongo_client, credentials)


@pytest.mark.parametrize("credentials", CREDENTIALS)
def test_stolen_secrets_encrypted(mongo_repository, mongo_client, credentials: Credentials):
    mongo_repository.save_stolen_credentials([credentials])
    check_if_stored_credentials_encrypted(mongo_client, credentials)


def check_if_stored_credentials_encrypted(mongo_client: MongoClient, original_credentials):
    original_credentials_mapping = original_credentials.dict(simplify=True)
    raw_credentials = get_all_credentials_in_mongo(mongo_client)

    for rc in raw_credentials:
        for identity_or_secret, credentials_component in rc.items():
            if original_credentials_mapping[identity_or_secret] is None:
                assert credentials_component is None
            else:
                for key, value in credentials_component.items():
                    if original_credentials_mapping[identity_or_secret][key] is not None:
                        assert original_credentials_mapping[identity_or_secret][key] != (
                            value.decode()
                        )
                        assert "***" not in value.decode()
                    else:
                        assert value is None

                    # Since secrets use the pydantic.SecretType, make sure we're not just storing
                    # all '*' characters.


def get_all_credentials_in_mongo(mongo_client: MongoClient) -> Iterable[Mapping[str, Any]]:
    encrypted_credentials = []

    # Loop through all databases and collections and search for credentials. We don't want the tests
    # to assume anything about the internal workings of the repository.
    for collection in get_all_collections_in_mongo(mongo_client):
        mongo_credentials = collection.find({})
        for mc in mongo_credentials:
            del mc["_id"]
            encrypted_credentials.append(mc)

    return encrypted_credentials

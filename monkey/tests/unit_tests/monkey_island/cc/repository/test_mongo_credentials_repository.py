import mongoengine
import pytest

from monkey_island.cc.repository import MongoCredentialsRepository


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

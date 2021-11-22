from unittest.mock import MagicMock

import mongomock
import pytest

from monkey_island.cc.setup.mongo.database_initializer import reset_database


@pytest.fixture
def patch_attack_mitigations_path(monkeypatch, data_for_tests_dir):
    def inner(file_name):
        path = data_for_tests_dir / "mongo_mitigations" / file_name
        monkeypatch.setattr(
            "monkey_island.cc.setup.mongo.database_initializer.ATTACK_MITIGATION_PATH", path
        )

    return inner


@pytest.fixture(scope="module", autouse=True)
def patch_dependencies(monkeypatch_session):
    monkeypatch_session.setattr(
        "monkey_island.cc.services.config.ConfigService.init_config", lambda: None
    )
    monkeypatch_session.setattr(
        "monkey_island.cc.services.database.jsonify", MagicMock(return_value=True)
    )


@pytest.fixture
def mock_mongo_client(monkeypatch):
    mongo = mongomock.MongoClient()
    mongo.db.validate_collection = MagicMock(return_value=True)

    monkeypatch.setattr("monkey_island.cc.setup.mongo.database_initializer.mongo", mongo)
    monkeypatch.setattr("monkey_island.cc.services.database.mongo", mongo)

    return mongo


def test_store_mitigations_on_mongo(patch_attack_mitigations_path, mock_mongo_client):
    patch_attack_mitigations_path("attack_mitigations.json")

    reset_database()

    assert len(list(mock_mongo_client.db.attack_mitigations.find({}))) == 3


def test_store_mitigations_on_mongo__invalid_mitigation(patch_attack_mitigations_path):
    patch_attack_mitigations_path("invalid_mitigation")

    with pytest.raises(Exception):
        reset_database()


def test_get_all_mitigations(mock_mongo_client):
    reset_database()

    mitigations = list(mock_mongo_client.db.attack_mitigations.find({}))

    assert len(mitigations) >= 266

    mitigation = mitigations[0]["mitigations"][0]
    assert mitigation["name"] is not None
    assert mitigation["description"] is not None
    assert mitigation["url"] is not None

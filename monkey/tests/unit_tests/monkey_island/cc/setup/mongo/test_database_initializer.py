import json.decoder
from pathlib import Path
from unittest.mock import MagicMock

import mongomock
import pytest

from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.setup.mongo.database_initializer import reset_database


@pytest.fixture
def fake_mongo(monkeypatch):
    mongo = mongomock.MongoClient()
    monkeypatch.setattr("monkey_island.cc.setup.mongo.database_initializer.mongo", mongo)
    monkeypatch.setattr("monkey_island.cc.services.database.mongo", mongo)
    return mongo


@pytest.fixture
def fake_config(monkeypatch):
    monkeypatch.setattr("monkey_island.cc.services.config.ConfigService.init_config", lambda: None)
    monkeypatch.setattr("monkey_island.cc.services.attack.attack_config.AttackConfig.reset_config", lambda: None)
    monkeypatch.setattr("monkey_island.cc.services.database.jsonify", MagicMock(return_value=True))


def test_store_mitigations_on_mongo(monkeypatch, data_for_tests_dir, fake_mongo, fake_config):
    monkeypatch.setattr(
        "monkey_island.cc.setup.mongo.database_initializer.ATTACK_MITIGATION_PATH",
        Path(data_for_tests_dir) / "mongo_mitigations" / "attack_mitigations.json",
    )
    fake_mongo.db.validate_collection = MagicMock(return_value=True)
    reset_database()

    assert len(list(fake_mongo.db.attack_mitigations.find({}))) == 3


def test_store_mitigations_on_mongo__invalid_mitigation(
    monkeypatch, data_for_tests_dir, fake_mongo, fake_config
):
    monkeypatch.setattr(
        "monkey_island.cc.setup.mongo.database_initializer.ATTACK_MITIGATION_PATH",
        Path(data_for_tests_dir) / "mongo_mitigations" / "invalid_mitigation",
    )
    fake_mongo.db.validate_collection = MagicMock(return_value=True)
    with pytest.raises(Exception):
        reset_database()


def test_get_all_mitigations():
    attack_mitigation_path = (
        Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "setup" / "mongo" / "attack_mitigations.json"
    )

    with open(attack_mitigation_path) as mitigations:
        mitigations = json.load(mitigations)["data"]
        assert len(mitigations) >= 266
        mitigation = next(iter(mitigations))["mitigations"][0]
        assert mitigation["name"] is not None
        assert mitigation["description"] is not None
        assert mitigation["url"] is not None
